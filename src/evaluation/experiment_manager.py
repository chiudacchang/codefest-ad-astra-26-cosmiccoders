"""Registro y consolidación de experimentos del sistema de recuperación."""

import csv
import json
import os
from datetime import datetime


CAMPOS = [
    "fecha",
    "responsable",
    "configuracion",
    "parametros",
    "duracion_segundos",
    "memoria_mb",
    "total_consultas",
    "ndcg_10",
    "f1_3",
    "errores",
    "observaciones",
    "conclusion",
]


def crear_registro(
    responsable,
    configuracion,
    parametros,
    duracion_segundos=0,
    memoria_mb=0,
    total_consultas=0,
    ndcg_10="",
    f1_3="",
    errores=0,
    observaciones="",
    conclusion="",
):
    """Organiza los datos de un experimento en un diccionario uniforme."""
    if isinstance(parametros, dict):
        parametros = json.dumps(parametros, ensure_ascii=False, sort_keys=True)

    return {
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "responsable": responsable,
        "configuracion": configuracion,
        "parametros": parametros,
        "duracion_segundos": duracion_segundos,
        "memoria_mb": memoria_mb,
        "total_consultas": total_consultas,
        "ndcg_10": ndcg_10,
        "f1_3": f1_3,
        "errores": errores,
        "observaciones": observaciones,
        "conclusion": conclusion,
    }


def guardar_registro(ruta_csv, registro):
    """Agrega un experimento al CSV y escribe encabezados cuando es nuevo."""
    carpeta = os.path.dirname(ruta_csv)
    if carpeta != "":
        os.makedirs(carpeta, exist_ok=True)

    archivo_nuevo = not os.path.exists(ruta_csv) or os.path.getsize(ruta_csv) == 0
    with open(ruta_csv, "a", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        if archivo_nuevo:
            escritor.writeheader()
        escritor.writerow(registro)


def leer_registros(ruta_csv):
    """Lee todos los experimentos de un archivo CSV."""
    if not os.path.isfile(ruta_csv):
        return []
    with open(ruta_csv, "r", encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


def numero_o_cero(valor):
    """Convierte un valor a float; retorna cero cuando no es numérico."""
    try:
        return float(valor)
    except (TypeError, ValueError):
        return 0.0


def consolidar_experimentos(rutas_csv):
    """Une varios registros y calcula indicadores generales."""
    registros = []
    for ruta in rutas_csv:
        registros.extend(leer_registros(ruta))

    cantidad = len(registros)
    suma_tiempo = 0.0
    suma_memoria = 0.0
    mejor_ndcg = 0.0
    mejor_f1 = 0.0

    for registro in registros:
        suma_tiempo += numero_o_cero(registro.get("duracion_segundos"))
        suma_memoria += numero_o_cero(registro.get("memoria_mb"))
        mejor_ndcg = max(mejor_ndcg, numero_o_cero(registro.get("ndcg_10")))
        mejor_f1 = max(mejor_f1, numero_o_cero(registro.get("f1_3")))

    return {
        "total_experimentos": cantidad,
        "tiempo_promedio_segundos": round(suma_tiempo / cantidad, 4)
        if cantidad
        else 0,
        "memoria_promedio_mb": round(suma_memoria / cantidad, 4)
        if cantidad
        else 0,
        "mejor_ndcg_10": mejor_ndcg,
        "mejor_f1_3": mejor_f1,
        "registros": registros,
    }


def guardar_consolidado(ruta_json, consolidado):
    """Guarda el consolidado para incluirlo en el informe técnico."""
    carpeta = os.path.dirname(ruta_json)
    if carpeta != "":
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta_json, "w", encoding="utf-8") as archivo:
        json.dump(consolidado, archivo, ensure_ascii=False, indent=4)
