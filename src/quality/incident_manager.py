"""Registro uniforme de incidentes encontrados durante las pruebas."""

import csv
import os
from datetime import datetime


CAMPOS_INCIDENTE = [
    "fecha",
    "componente",
    "severidad",
    "descripcion",
    "pasos_reproduccion",
    "resultado_esperado",
    "resultado_obtenido",
    "estado",
    "responsable",
    "solucion",
]


def crear_incidente(
    componente,
    severidad,
    descripcion,
    pasos_reproduccion,
    resultado_esperado,
    resultado_obtenido,
    responsable="Chiu",
    estado="abierto",
    solucion="",
):
    """Crea un diccionario con todos los datos necesarios para reproducir un error."""
    return {
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "componente": componente,
        "severidad": severidad,
        "descripcion": descripcion,
        "pasos_reproduccion": pasos_reproduccion,
        "resultado_esperado": resultado_esperado,
        "resultado_obtenido": resultado_obtenido,
        "estado": estado,
        "responsable": responsable,
        "solucion": solucion,
    }


def guardar_incidente(ruta_csv, incidente):
    """Agrega el incidente a un CSV compartido por el equipo."""
    carpeta = os.path.dirname(ruta_csv)
    if carpeta != "":
        os.makedirs(carpeta, exist_ok=True)
    archivo_nuevo = not os.path.exists(ruta_csv) or os.path.getsize(ruta_csv) == 0

    with open(ruta_csv, "a", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_INCIDENTE)
        if archivo_nuevo:
            escritor.writeheader()
        escritor.writerow(incidente)
