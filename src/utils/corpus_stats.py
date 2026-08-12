"""Funciones para calcular estadísticas sencillas de cada documento."""

import os


EXTENSIONES_TEXTO = (".txt", ".md", ".csv", ".json", ".html", ".htm")


def extraer_texto_pdf(ruta_archivo):
    """Extrae y une el texto de todas las páginas de un PDF."""
    from pypdf import PdfReader

    lector = PdfReader(ruta_archivo)
    texto_completo = ""

    for pagina in lector.pages:
        texto_pagina = pagina.extract_text()
        if texto_pagina is not None:
            texto_completo += texto_pagina + "\n"

    return texto_completo


def extraer_texto(ruta_archivo):
    """Extrae texto de los formatos compatibles en este primer avance."""
    extension = os.path.splitext(ruta_archivo)[1].lower()

    if extension == ".pdf":
        return extraer_texto_pdf(ruta_archivo)

    if extension in EXTENSIONES_TEXTO:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return archivo.read()

    return ""


def detectar_idioma(texto):
    """Detecta el idioma del texto con langdetect cuando hay texto suficiente."""
    if texto.strip() == "":
        return "desconocido"

    try:
        from langdetect import detect

        return detect(texto)
    except ImportError:
        return "desconocido"
    except Exception:
        return "desconocido"


def extraer_estadisticas(ruta_archivo):
    """Calcula formato, caracteres, palabras e idioma de un archivo válido."""
    extension = os.path.splitext(ruta_archivo)[1].lower()
    formato = extension.replace(".", "")

    estadisticas = {
        "formato": formato,
        "total_caracteres": 0,
        "total_palabras": 0,
        "idioma": "desconocido",
    }

    try:
        texto_limpio = extraer_texto(ruta_archivo)
    except Exception:
        texto_limpio = ""

    estadisticas["total_caracteres"] = len(texto_limpio)
    estadisticas["total_palabras"] = len(texto_limpio.split())
    estadisticas["idioma"] = detectar_idioma(texto_limpio)

    return estadisticas
