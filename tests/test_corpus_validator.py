"""Pruebas básicas para las funciones de validación del corpus."""

import json
import os
import sys
import tempfile
import unittest

from pypdf import PdfWriter


RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_UTILIDADES = os.path.join(RUTA_PROYECTO, "src", "utils")
sys.path.insert(0, RUTA_UTILIDADES)

from corpus_validator import archivo_valido
from run_validation import procesar_corpus


class PruebasValidadorCorpus(unittest.TestCase):
    """Agrupa casos de prueba que representan situaciones comunes del corpus."""

    def test_rechaza_archivo_vacio(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "vacio.txt")
            open(ruta, "w", encoding="utf-8").close()

            valido, mensaje = archivo_valido(ruta)

            self.assertFalse(valido)
            self.assertIn("vacío", mensaje)

    def test_acepta_archivo_texto_utf8(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "documento.txt")
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("La seguridad espacial requiere cooperación internacional.")

            valido, mensaje = archivo_valido(ruta)

            self.assertTrue(valido)
            self.assertEqual(mensaje, "Archivo de texto válido")

    def test_rechaza_json_incorrecto(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "datos.json")
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write('{"documento": }')

            valido, mensaje = archivo_valido(ruta)

            self.assertFalse(valido)
            self.assertIn("estructura incorrecta", mensaje)

    def test_acepta_pdf_con_una_pagina(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "documento.pdf")
            escritor = PdfWriter()
            escritor.add_blank_page(width=300, height=300)

            with open(ruta, "wb") as archivo:
                escritor.write(archivo)

            valido, mensaje = archivo_valido(ruta)

            self.assertTrue(valido)
            self.assertEqual(mensaje, "Archivo PDF válido")

    def test_rechaza_pdf_corrupto(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "corrupto.pdf")
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("Este contenido no tiene la estructura de un PDF.")

            valido, mensaje = archivo_valido(ruta)

            self.assertFalse(valido)
            self.assertIn("no se pudo abrir", mensaje)

    def test_genera_reportes_del_corpus(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta_corpus = os.path.join(carpeta, "corpus")
            ruta_resultados = os.path.join(carpeta, "resultados")
            os.makedirs(ruta_corpus)

            with open(
                os.path.join(ruta_corpus, "documento.txt"),
                "w",
                encoding="utf-8",
            ) as archivo:
                archivo.write("Documento de prueba sobre órbita terrestre baja.")

            reporte = procesar_corpus(ruta_corpus, ruta_resultados)

            self.assertEqual(reporte["resumen_general"]["total_archivos_validos"], 1)
            self.assertTrue(
                os.path.exists(os.path.join(ruta_resultados, "estadisticas.json"))
            )
            self.assertTrue(
                os.path.exists(os.path.join(ruta_resultados, "reporte_errores.json"))
            )

            with open(
                os.path.join(ruta_resultados, "estadisticas.json"),
                "r",
                encoding="utf-8",
            ) as archivo:
                informacion_guardada = json.load(archivo)

            self.assertEqual(
                informacion_guardada["resumen_general"]["total_archivos_validos"],
                1,
            )

    def test_ignora_archivos_ocultos_de_git(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta_corpus = os.path.join(carpeta, "corpus")
            ruta_resultados = os.path.join(carpeta, "resultados")
            os.makedirs(ruta_corpus)

            with open(
                os.path.join(ruta_corpus, ".gitkeep"),
                "w",
                encoding="utf-8",
            ) as archivo:
                archivo.write("archivo técnico")

            reporte = procesar_corpus(ruta_corpus, ruta_resultados)

            self.assertEqual(reporte["resumen_general"]["total_archivos_validos"], 0)


if __name__ == "__main__":
    unittest.main()
