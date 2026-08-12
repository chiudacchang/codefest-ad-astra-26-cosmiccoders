"""Cálculo reproducible de NDCG@10 para fragmentos y F1@3 para documentos."""

import json
import math
import os
import sys


def normalizar_texto(texto):
    """Normaliza espacios y mayúsculas para comparar contenido textual."""
    return " ".join(str(texto).lower().split())


def calcular_dcg(relevancias, limite=10):
    """Calcula Discounted Cumulative Gain con la fórmula oficial del reto."""
    dcg = 0.0
    for posicion in range(min(len(relevancias), limite)):
        relevancia = relevancias[posicion]
        dcg += relevancia / math.log2(posicion + 2)
    return dcg


def calcular_ndcg(relevancias_obtenidas, relevancias_ideales, limite=10):
    """Divide el DCG obtenido por el DCG del orden ideal."""
    dcg = calcular_dcg(relevancias_obtenidas, limite)
    orden_ideal = sorted(relevancias_ideales, reverse=True)
    idcg = calcular_dcg(orden_ideal, limite)
    if idcg == 0:
        return 0.0
    return dcg / idcg


def calcular_f1_documentos(documentos_obtenidos, documentos_relevantes):
    """Calcula F1@3 como métrica de conjunto, sin considerar el orden."""
    obtenidos = set(documentos_obtenidos[:3])
    relevantes = set(documentos_relevantes)
    aciertos = len(obtenidos.intersection(relevantes))

    precision = aciertos / 3
    denominador_recall = min(len(relevantes), 3)
    recall = aciertos / denominador_recall if denominador_recall > 0 else 0

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    return {"precision_3": precision, "recall_3": recall, "f1_3": f1}


def leer_jsonl(ruta_archivo):
    """Lee objetos JSON separados por líneas."""
    objetos = []
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if linea.strip() != "":
                objetos.append(json.loads(linea))
    return objetos


def indexar_por_query_id(objetos):
    """Convierte una lista de consultas en un diccionario por query_id."""
    indice = {}
    for objeto in objetos:
        indice[objeto["query_id"]] = objeto
    return indice


def relevancias_fragmentos(resultado, juicio):
    """Busca la relevancia de cada texto entregado en los juicios manuales."""
    mapa = {}
    for fragmento in juicio.get("relevant_fragments", []):
        texto = normalizar_texto(fragmento.get("text", ""))
        mapa[texto] = float(fragmento.get("relevance", 0))

    obtenidas = []
    for fragmento in resultado.get("fragments", [])[:10]:
        texto = normalizar_texto(fragmento.get("text", ""))
        obtenidas.append(mapa.get(texto, 0.0))

    ideales = list(mapa.values())
    return obtenidas, ideales


def evaluar_resultados(ruta_resultados, ruta_juicios):
    """Evalúa resultados contra juicios manuales u oficiales disponibles."""
    resultados = indexar_por_query_id(leer_jsonl(ruta_resultados))
    juicios = indexar_por_query_id(leer_jsonl(ruta_juicios))
    detalles = []
    suma_ndcg = 0.0
    suma_f1 = 0.0

    for query_id in sorted(juicios.keys()):
        if query_id not in resultados:
            detalles.append({"query_id": query_id, "error": "Falta el resultado"})
            continue

        resultado = resultados[query_id]
        juicio = juicios[query_id]
        obtenidas, ideales = relevancias_fragmentos(resultado, juicio)
        ndcg = calcular_ndcg(obtenidas, ideales, 10)
        documentos = [
            elemento.get("doc_id", "")
            for elemento in resultado.get("documents", [])[:3]
        ]
        metricas_documentos = calcular_f1_documentos(
            documentos, juicio.get("relevant_documents", [])
        )

        suma_ndcg += ndcg
        suma_f1 += metricas_documentos["f1_3"]
        detalles.append(
            {
                "query_id": query_id,
                "ndcg_10": round(ndcg, 6),
                "precision_3": round(metricas_documentos["precision_3"], 6),
                "recall_3": round(metricas_documentos["recall_3"], 6),
                "f1_3": round(metricas_documentos["f1_3"], 6),
            }
        )

    cantidad = len(juicios)
    return {
        "total_consultas_evaluadas": cantidad,
        "promedio_ndcg_10": round(suma_ndcg / cantidad, 6) if cantidad else 0,
        "promedio_f1_3": round(suma_f1 / cantidad, 6) if cantidad else 0,
        "detalles": detalles,
    }


def main():
    """Ejecuta las métricas con dos rutas recibidas por consola."""
    if len(sys.argv) < 3:
        print(
            "Uso: python src/evaluation/retrieval_metrics.py "
            "RESULTADOS.jsonl JUICIOS.jsonl"
        )
        return

    reporte = evaluar_resultados(sys.argv[1], sys.argv[2])
    os.makedirs("results", exist_ok=True)
    with open("results/metricas_recuperacion.json", "w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, ensure_ascii=False, indent=4)
    print("NDCG@10 promedio:", reporte["promedio_ndcg_10"])
    print("F1@3 promedio:", reporte["promedio_f1_3"])


if __name__ == "__main__":
    main()
