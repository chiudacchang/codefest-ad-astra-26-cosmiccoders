"""Validación estricta del archivo resultados.jsonl exigido por CODEFEST."""

import json
import os
import sys


def leer_jsonl(ruta_archivo):
    """Lee cada línea JSON y registra los errores sin detener la revisión."""
    objetos = []
    errores = []

    if not os.path.isfile(ruta_archivo):
        return objetos, ["No existe el archivo " + ruta_archivo]

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        numero_linea = 0
        for linea in archivo:
            numero_linea += 1
            if linea.strip() == "":
                errores.append("La línea " + str(numero_linea) + " está vacía")
            else:
                try:
                    objetos.append(json.loads(linea))
                except json.JSONDecodeError:
                    errores.append(
                        "La línea " + str(numero_linea) + " no contiene JSON válido"
                    )

    return objetos, errores


def validar_ranks(elementos, cantidad, nombre, query_id):
    """Comprueba cantidad y ranks consecutivos de una lista de resultados."""
    errores = []
    if not isinstance(elementos, list):
        return [query_id + ": " + nombre + " debe ser una lista"]

    if len(elementos) != cantidad:
        errores.append(
            query_id
            + ": "
            + nombre
            + " debe contener exactamente "
            + str(cantidad)
            + " elementos"
        )

    limite = min(len(elementos), cantidad)
    for posicion in range(limite):
        rank_esperado = posicion + 1
        if not isinstance(elementos[posicion], dict):
            errores.append(
                query_id
                + ": el elemento de "
                + nombre
                + " en la posición "
                + str(rank_esperado)
                + " debe ser un objeto JSON"
            )
            continue
        if elementos[posicion].get("rank") != rank_esperado:
            errores.append(
                query_id
                + ": el rank de "
                + nombre
                + " en la posición "
                + str(rank_esperado)
                + " es incorrecto"
            )
    return errores


def validar_consulta(resultado, query_id_esperado):
    """Valida un objeto de resultado correspondiente a una consulta."""
    errores = []
    advertencias = []
    if not isinstance(resultado, dict):
        return [query_id_esperado + ": el resultado debe ser un objeto JSON"], []

    query_id = str(resultado.get("query_id", "sin_query_id"))

    if query_id != query_id_esperado:
        errores.append(
            "Se esperaba " + query_id_esperado + " y se encontró " + query_id
        )

    documentos = resultado.get("documents")
    fragmentos = resultado.get("fragments")
    errores.extend(validar_ranks(documentos, 3, "documents", query_id))
    errores.extend(validar_ranks(fragmentos, 10, "fragments", query_id))

    if isinstance(documentos, list):
        documentos_vistos = set()
        for documento in documentos:
            if not isinstance(documento, dict):
                continue
            doc_id = str(documento.get("doc_id", "")).strip()
            if doc_id == "":
                errores.append(query_id + ": un documento no tiene doc_id")
            elif doc_id in documentos_vistos:
                errores.append(query_id + ": hay doc_id duplicados en documents")
            else:
                documentos_vistos.add(doc_id)

    if isinstance(fragmentos, list):
        for fragmento in fragmentos:
            if not isinstance(fragmento, dict):
                continue
            campos = ("rank", "chunk_id", "doc_id", "text")
            for campo in campos:
                if campo not in fragmento:
                    errores.append(
                        query_id + ": falta el campo " + campo + " en fragments"
                    )

            texto = str(fragmento.get("text", "")).strip()
            if texto == "":
                errores.append(query_id + ": hay un fragmento sin texto")
            elif len(texto.split()) > 250:
                errores.append(query_id + ": un fragmento supera 250 palabras")

            if str(fragmento.get("chunk_id", "")).strip() == "":
                errores.append(query_id + ": hay un fragmento sin chunk_id")
            if str(fragmento.get("doc_id", "")).strip() == "":
                errores.append(query_id + ": hay un fragmento sin doc_id")

    return errores, advertencias


def validar_resultados(ruta_archivo, total_consultas=50):
    """Valida las 50 líneas y el esquema oficial de resultados.jsonl."""
    resultados, errores = leer_jsonl(ruta_archivo)
    advertencias = []

    if len(resultados) != total_consultas:
        errores.append(
            "El archivo debe contener exactamente "
            + str(total_consultas)
            + " objetos JSON"
        )

    limite = min(len(resultados), total_consultas)
    for posicion in range(limite):
        query_id = "q" + str(posicion + 1).zfill(3)
        errores_consulta, advertencias_consulta = validar_consulta(
            resultados[posicion], query_id
        )
        errores.extend(errores_consulta)
        advertencias.extend(advertencias_consulta)

    return {
        "valido": len(errores) == 0,
        "total_lineas_validas": len(resultados),
        "total_errores": len(errores),
        "total_advertencias": len(advertencias),
        "errores": errores,
        "advertencias": advertencias,
    }


def main():
    """Valida una ruta recibida o resultados.jsonl por defecto."""
    ruta = "resultados.jsonl"
    if len(sys.argv) > 1:
        ruta = sys.argv[1]

    reporte = validar_resultados(ruta)
    os.makedirs("results", exist_ok=True)
    with open("results/validacion_resultados.json", "w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, ensure_ascii=False, indent=4)

    if reporte["valido"]:
        print("El archivo resultados.jsonl cumple el esquema oficial")
    else:
        print("El archivo tiene", reporte["total_errores"], "errores")


if __name__ == "__main__":
    main()
