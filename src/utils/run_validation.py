"""Programa principal para validar el corpus y generar sus estadísticas."""

import json
import os
import sys

from corpus_stats import extraer_estadisticas
from corpus_validator import archivo_valido


def aumentar_contador(diccionario, clave):
    """Suma uno al contador de una clave dentro de un diccionario."""
    if clave in diccionario:
        diccionario[clave] += 1
    else:
        diccionario[clave] = 1


def guardar_json(ruta_archivo, informacion):
    """Guarda un diccionario o una lista en un archivo JSON."""
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(informacion, archivo, ensure_ascii=False, indent=4)


def procesar_corpus(ruta_raw, ruta_resultados):
    """Valida todos los archivos de una carpeta y construye el reporte final."""
    detalles_archivos = []
    archivos_rechazados = []
    formatos = {}
    idiomas = {}
    total_palabras = 0
    total_caracteres = 0

    if not os.path.isdir(ruta_raw):
        print("Error: no se encontró la carpeta " + ruta_raw)
        return None

    for carpeta_actual, carpetas, archivos in os.walk(ruta_raw):
        carpetas.sort()
        archivos.sort()

        for nombre_archivo in archivos:
            if nombre_archivo.startswith("."):
                continue

            ruta_archivo = os.path.join(carpeta_actual, nombre_archivo)
            ruta_relativa = os.path.relpath(ruta_archivo, ruta_raw)
            valido, mensaje = archivo_valido(ruta_archivo)

            if valido:
                estadisticas = extraer_estadisticas(ruta_archivo)
                estadisticas["archivo"] = ruta_relativa
                estadisticas["estado_validacion"] = mensaje
                detalles_archivos.append(estadisticas)

                total_palabras += estadisticas["total_palabras"]
                total_caracteres += estadisticas["total_caracteres"]
                aumentar_contador(formatos, estadisticas["formato"])
                aumentar_contador(idiomas, estadisticas["idioma"])
            else:
                archivos_rechazados.append(
                    {"archivo": ruta_relativa, "error": mensaje}
                )

    cantidad_validos = len(detalles_archivos)

    if cantidad_validos > 0:
        promedio_palabras = total_palabras / cantidad_validos
        promedio_caracteres = total_caracteres / cantidad_validos
    else:
        promedio_palabras = 0
        promedio_caracteres = 0

    reporte_final = {
        "resumen_general": {
            "total_archivos_validos": cantidad_validos,
            "total_archivos_rechazados": len(archivos_rechazados),
            "promedio_palabras_por_documento": round(promedio_palabras, 2),
            "promedio_caracteres_por_documento": round(promedio_caracteres, 2),
            "distribucion_formatos": formatos,
            "distribucion_idiomas": idiomas,
        },
        "detalles_archivos": detalles_archivos,
        "archivos_rechazados": archivos_rechazados,
    }

    os.makedirs(ruta_resultados, exist_ok=True)
    guardar_json(os.path.join(ruta_resultados, "estadisticas.json"), reporte_final)
    guardar_json(
        os.path.join(ruta_resultados, "reporte_errores.json"),
        archivos_rechazados,
    )

    return reporte_final


def main():
    """Define las rutas, ejecuta la validación e informa el resultado."""
    ruta_raw = "data/raw"
    ruta_resultados = "results"

    if len(sys.argv) > 1:
        ruta_raw = sys.argv[1]

    reporte = procesar_corpus(ruta_raw, ruta_resultados)

    if reporte is not None:
        resumen = reporte["resumen_general"]
        print("Validación terminada")
        print("Archivos válidos:", resumen["total_archivos_validos"])
        print("Archivos rechazados:", resumen["total_archivos_rechazados"])
        print("Reportes guardados en la carpeta results")


if __name__ == "__main__":
    main()
