"""Evaluación automática de la calidad básica de los chunks."""

import json
import os
import random
import sys


def cargar_objetos_json(ruta_archivo):
    """Carga uno o varios objetos desde un archivo JSON o JSON Lines."""
    objetos = []
    extension = os.path.splitext(ruta_archivo)[1].lower()

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        if extension == ".jsonl":
            numero_linea = 0
            for linea in archivo:
                numero_linea += 1
                if linea.strip() != "":
                    try:
                        objetos.append(json.loads(linea))
                    except json.JSONDecodeError:
                        objetos.append(
                            {
                                "_error_carga": "JSON inválido en la línea "
                                + str(numero_linea),
                                "_archivo": ruta_archivo,
                            }
                        )
        else:
            informacion = json.load(archivo)
            if isinstance(informacion, list):
                objetos.extend(informacion)
            else:
                objetos.append(informacion)

    return objetos


def cargar_chunks(ruta_entrada):
    """Carga chunks desde un archivo o desde todos los JSON de una carpeta."""
    chunks = []

    if os.path.isfile(ruta_entrada):
        return cargar_objetos_json(ruta_entrada)

    if not os.path.isdir(ruta_entrada):
        return chunks

    for carpeta_actual, carpetas, archivos in os.walk(ruta_entrada):
        carpetas.sort()
        archivos.sort()
        for nombre in archivos:
            extension = os.path.splitext(nombre)[1].lower()
            if extension in (".json", ".jsonl"):
                ruta_archivo = os.path.join(carpeta_actual, nombre)
                try:
                    chunks.extend(cargar_objetos_json(ruta_archivo))
                except Exception as error:
                    chunks.append(
                        {
                            "_error_carga": str(error),
                            "_archivo": ruta_archivo,
                        }
                    )

    return chunks


def obtener_texto(chunk):
    """Busca el texto aunque el equipo use 'texto' o 'text' como nombre."""
    if "texto" in chunk:
        return str(chunk["texto"])
    if "text" in chunk:
        return str(chunk["text"])
    if "contenido" in chunk:
        return str(chunk["contenido"])
    return ""


def contar_palabras(texto):
    """Cuenta palabras separando el texto por espacios."""
    return len(texto.split())


def parece_completo(texto):
    """Aplica una regla sencilla para detectar posibles oraciones cortadas."""
    texto = texto.strip()
    if texto == "":
        return False
    finales_validos = (".", "?", "!", ":", ";", '"', "'", ")", "]")
    return texto.endswith(finales_validos)


def agregar_hallazgo(lista, nivel, tipo, mensaje):
    """Agrega un hallazgo con nivel, tipo y explicación."""
    lista.append({"nivel": nivel, "tipo": tipo, "mensaje": mensaje})


def evaluar_chunks(chunks, minimo_palabras=20, maximo_palabras=250):
    """Evalúa campos, tamaños, duplicados y completitud de una lista de chunks."""
    detalles = []
    identificadores_vistos = set()
    textos_vistos = set()
    total_palabras = 0
    minimo_encontrado = None
    maximo_encontrado = 0
    total_errores = 0
    total_advertencias = 0

    for posicion in range(len(chunks)):
        chunk = chunks[posicion]
        hallazgos = []
        if not isinstance(chunk, dict):
            detalles.append(
                {
                    "posicion": posicion + 1,
                    "chunk_id": "",
                    "doc_id": "",
                    "total_palabras": 0,
                    "hallazgos": [
                        {
                            "nivel": "error",
                            "tipo": "estructura",
                            "mensaje": "El chunk debe ser un objeto JSON",
                        }
                    ],
                }
            )
            total_errores += 1
            continue

        chunk_id = chunk.get("chunk_id", "")
        doc_id = chunk.get("doc_id", "")
        texto = obtener_texto(chunk).strip()
        palabras = contar_palabras(texto)

        if "_error_carga" in chunk:
            agregar_hallazgo(
                hallazgos, "error", "carga", str(chunk["_error_carga"])
            )

        if chunk_id == "":
            agregar_hallazgo(
                hallazgos, "error", "chunk_id", "Falta el identificador del chunk"
            )
        elif chunk_id in identificadores_vistos:
            agregar_hallazgo(
                hallazgos, "error", "chunk_id", "El chunk_id está duplicado"
            )
        else:
            identificadores_vistos.add(chunk_id)

        if doc_id == "":
            agregar_hallazgo(
                hallazgos, "error", "doc_id", "Falta el documento de origen"
            )

        if texto == "":
            agregar_hallazgo(hallazgos, "error", "texto", "El chunk está vacío")
        else:
            texto_normalizado = " ".join(texto.lower().split())
            if texto_normalizado in textos_vistos:
                agregar_hallazgo(
                    hallazgos, "advertencia", "duplicado", "El texto está repetido"
                )
            else:
                textos_vistos.add(texto_normalizado)

            if palabras < minimo_palabras:
                agregar_hallazgo(
                    hallazgos,
                    "advertencia",
                    "longitud",
                    "El chunk tiene menos de " + str(minimo_palabras) + " palabras",
                )

            if palabras > maximo_palabras:
                agregar_hallazgo(
                    hallazgos,
                    "advertencia",
                    "longitud",
                    "El chunk supera " + str(maximo_palabras) + " palabras",
                )

            if not parece_completo(texto):
                agregar_hallazgo(
                    hallazgos,
                    "advertencia",
                    "completitud",
                    "El texto podría terminar con una oración cortada",
                )

        for hallazgo in hallazgos:
            if hallazgo["nivel"] == "error":
                total_errores += 1
            else:
                total_advertencias += 1

        total_palabras += palabras
        if minimo_encontrado is None or palabras < minimo_encontrado:
            minimo_encontrado = palabras
        if palabras > maximo_encontrado:
            maximo_encontrado = palabras

        detalles.append(
            {
                "posicion": posicion + 1,
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "total_palabras": palabras,
                "hallazgos": hallazgos,
            }
        )

    cantidad = len(chunks)
    promedio = total_palabras / cantidad if cantidad > 0 else 0
    if minimo_encontrado is None:
        minimo_encontrado = 0

    return {
        "resumen": {
            "total_chunks": cantidad,
            "total_errores": total_errores,
            "total_advertencias": total_advertencias,
            "promedio_palabras": round(promedio, 2),
            "minimo_palabras": minimo_encontrado,
            "maximo_palabras": maximo_encontrado,
            "limite_salida_oficial": maximo_palabras,
        },
        "detalles": detalles,
    }


def seleccionar_muestra(chunks, cantidad=10, semilla=42):
    """Selecciona una muestra reproducible para revisión manual."""
    if len(chunks) <= cantidad:
        return chunks.copy()
    random.seed(semilla)
    return random.sample(chunks, cantidad)


def guardar_reporte(reporte, ruta_salida):
    """Guarda el reporte de calidad en JSON."""
    carpeta = os.path.dirname(ruta_salida)
    if carpeta != "":
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, ensure_ascii=False, indent=4)


def main():
    """Ejecuta la evaluación desde la línea de comandos."""
    if len(sys.argv) < 2:
        print("Uso: python src/quality/chunk_quality.py RUTA_CHUNKS")
        return

    chunks = cargar_chunks(sys.argv[1])
    reporte = evaluar_chunks(chunks)
    reporte["muestra_revision_manual"] = seleccionar_muestra(chunks)
    guardar_reporte(reporte, "results/calidad_chunks.json")
    print("Chunks evaluados:", reporte["resumen"]["total_chunks"])
    print("Errores:", reporte["resumen"]["total_errores"])
    print("Advertencias:", reporte["resumen"]["total_advertencias"])


if __name__ == "__main__":
    main()
