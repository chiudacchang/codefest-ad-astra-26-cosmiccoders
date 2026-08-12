"""Pruebas para el análisis de calidad de chunks."""

import os
import sys
import unittest


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src", "quality"))

from chunk_quality import evaluar_chunks, seleccionar_muestra


class PruebasCalidadChunks(unittest.TestCase):
    def test_detecta_chunk_vacio(self):
        chunks = [{"chunk_id": "c1", "doc_id": "d1", "texto": ""}]
        reporte = evaluar_chunks(chunks)
        self.assertGreater(reporte["resumen"]["total_errores"], 0)

    def test_detecta_identificador_duplicado(self):
        texto = "Esta es una oración completa con suficiente contenido. " * 5
        chunks = [
            {"chunk_id": "c1", "doc_id": "d1", "texto": texto},
            {"chunk_id": "c1", "doc_id": "d1", "texto": texto + "Otra oración."},
        ]
        reporte = evaluar_chunks(chunks)
        tipos = []
        for detalle in reporte["detalles"]:
            for hallazgo in detalle["hallazgos"]:
                tipos.append(hallazgo["tipo"])
        self.assertIn("chunk_id", tipos)

    def test_detecta_fragmento_mayor_a_250_palabras(self):
        texto = ("palabra " * 251).strip() + "."
        chunks = [{"chunk_id": "c1", "doc_id": "d1", "text": texto}]
        reporte = evaluar_chunks(chunks)
        mensajes = reporte["detalles"][0]["hallazgos"]
        self.assertTrue(any(h["tipo"] == "longitud" for h in mensajes))

    def test_muestra_es_reproducible(self):
        chunks = [{"chunk_id": str(i)} for i in range(20)]
        muestra_1 = seleccionar_muestra(chunks, 5, 42)
        muestra_2 = seleccionar_muestra(chunks, 5, 42)
        self.assertEqual(muestra_1, muestra_2)

    def test_rechaza_chunk_que_no_es_diccionario(self):
        reporte = evaluar_chunks(["texto sin estructura"])
        self.assertEqual(reporte["resumen"]["total_errores"], 1)


if __name__ == "__main__":
    unittest.main()
