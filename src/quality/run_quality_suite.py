"""Punto de entrada para ejecutar las revisiones disponibles del integrante 4."""

import json
import os
import sys

from chunk_quality import cargar_chunks, evaluar_chunks, seleccionar_muestra
from performance_monitor import medir_funcion
from project_audit import auditar_proyecto
from results_validator import validar_resultados


def guardar_json(ruta, informacion):
    """Guarda un reporte JSON creando primero su carpeta."""
    carpeta = os.path.dirname(ruta)
    if carpeta != "":
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(informacion, archivo, ensure_ascii=False, indent=4)


def ejecutar_suite(ruta_chunks="", ruta_resultados=""):
    """Ejecuta solo las pruebas cuyos insumos ya existen."""
    reporte_general = {"pruebas_ejecutadas": [], "pruebas_pendientes": []}

    auditoria_medida = medir_funcion(auditar_proyecto, ".")
    guardar_json("results/auditoria_proyecto.json", auditoria_medida["resultado"])
    reporte_general["pruebas_ejecutadas"].append(
        {
            "nombre": "auditoria_proyecto",
            "duracion_segundos": auditoria_medida["duracion_segundos"],
            "memoria_maxima_mb": auditoria_medida["memoria_maxima_mb"],
        }
    )

    if ruta_chunks != "" and os.path.exists(ruta_chunks):
        chunks = cargar_chunks(ruta_chunks)
        calidad_medida = medir_funcion(evaluar_chunks, chunks)
        calidad = calidad_medida["resultado"]
        calidad["muestra_revision_manual"] = seleccionar_muestra(chunks)
        guardar_json("results/calidad_chunks.json", calidad)
        reporte_general["pruebas_ejecutadas"].append(
            {
                "nombre": "calidad_chunks",
                "duracion_segundos": calidad_medida["duracion_segundos"],
                "memoria_maxima_mb": calidad_medida["memoria_maxima_mb"],
            }
        )
    else:
        reporte_general["pruebas_pendientes"].append(
            "Calidad de chunks: todavía no existe el insumo"
        )

    if ruta_resultados != "" and os.path.isfile(ruta_resultados):
        resultados_medidos = medir_funcion(validar_resultados, ruta_resultados)
        guardar_json(
            "results/validacion_resultados.json", resultados_medidos["resultado"]
        )
        reporte_general["pruebas_ejecutadas"].append(
            {
                "nombre": "validacion_resultados",
                "duracion_segundos": resultados_medidos["duracion_segundos"],
                "memoria_maxima_mb": resultados_medidos["memoria_maxima_mb"],
            }
        )
    else:
        reporte_general["pruebas_pendientes"].append(
            "Validación de resultados: todavía no existe resultados.jsonl"
        )

    guardar_json("results/reporte_suite_calidad.json", reporte_general)
    return reporte_general


def main():
    """Recibe opcionalmente las rutas de chunks y resultados."""
    ruta_chunks = sys.argv[1] if len(sys.argv) > 1 else "data/chunks"
    ruta_resultados = sys.argv[2] if len(sys.argv) > 2 else "resultados.jsonl"
    reporte = ejecutar_suite(ruta_chunks, ruta_resultados)
    print("Pruebas ejecutadas:", len(reporte["pruebas_ejecutadas"]))
    print("Pruebas pendientes:", len(reporte["pruebas_pendientes"]))


if __name__ == "__main__":
    main()
