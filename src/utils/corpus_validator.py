"""Funciones para comprobar si los archivos del corpus se pueden procesar."""

import json
import os
import zipfile


EXTENSIONES_TEXTO = (".txt", ".md", ".csv", ".json", ".html", ".htm")


def validar_archivo_texto(ruta_archivo):
    """Comprueba que un archivo de texto se pueda leer usando UTF-8."""
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
    except UnicodeDecodeError:
        return False, "El archivo no usa una codificación UTF-8 válida"
    except OSError as error:
        return False, "No fue posible leer el archivo: " + str(error)

    if contenido.strip() == "":
        return False, "El archivo no contiene texto útil"

    return True, "Archivo de texto válido"


def validar_archivo_json(ruta_archivo):
    """Comprueba que el contenido de un archivo JSON tenga una estructura válida."""
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            json.load(archivo)
    except UnicodeDecodeError:
        return False, "El archivo no usa una codificación UTF-8 válida"
    except json.JSONDecodeError:
        return False, "El archivo JSON tiene una estructura incorrecta"
    except OSError as error:
        return False, "No fue posible leer el archivo: " + str(error)

    return True, "Archivo JSON válido"


def validar_archivo_pdf(ruta_archivo):
    """Intenta abrir el PDF y consultar su cantidad de páginas."""
    try:
        from pypdf import PdfReader

        lector = PdfReader(ruta_archivo)
        cantidad_paginas = len(lector.pages)
    except ImportError:
        return False, "Falta instalar la librería pypdf"
    except Exception as error:
        return False, "El PDF no se pudo abrir: " + str(error)

    if cantidad_paginas == 0:
        return False, "El PDF no contiene páginas"

    return True, "Archivo PDF válido"


def validar_archivo_xlsx(ruta_archivo):
    """Comprueba la estructura básica de un archivo XLSX."""
    if zipfile.is_zipfile(ruta_archivo):
        return True, "Archivo XLSX válido"

    return False, "El archivo XLSX tiene una estructura incorrecta"


def archivo_valido(ruta_archivo):
    """Retorna una tupla que indica si el archivo es válido y explica el resultado."""
    if not os.path.exists(ruta_archivo):
        return False, "El archivo no existe"

    if not os.path.isfile(ruta_archivo):
        return False, "La ruta recibida no corresponde a un archivo"

    try:
        tamaño_archivo = os.path.getsize(ruta_archivo)
    except OSError as error:
        return False, "No fue posible consultar el archivo: " + str(error)

    if tamaño_archivo == 0:
        return False, "El archivo está vacío"

    extension = os.path.splitext(ruta_archivo)[1].lower()

    if extension == ".json":
        return validar_archivo_json(ruta_archivo)

    if extension in EXTENSIONES_TEXTO:
        return validar_archivo_texto(ruta_archivo)

    if extension == ".pdf":
        return validar_archivo_pdf(ruta_archivo)

    if extension == ".xlsx":
        return validar_archivo_xlsx(ruta_archivo)

    return True, "Archivo no vacío; su formato requiere una revisión posterior"
