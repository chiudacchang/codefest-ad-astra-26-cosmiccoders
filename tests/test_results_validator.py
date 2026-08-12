"""Pruebas del esquema oficial de resultados.jsonl."""

import json
import os
import sys
import tempfile
import unittest


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src", "quality"))

from results_validator import validar_resultados


def crear_resultado(query_id):
    documentos = []
    fragmentos = []
    for rank in range(1, 4):
        documentos.append({"rank": rank, "doc_id": "DOC-" + str(rank)})
    for rank in range(1, 11):
        fragmentos.append(
            {
                "rank": rank,
                "chunk_id": "CHUNK-" + str(rank),
                "doc_id": "DOC-" + str(((rank - 1) % 3) + 1),
                "text": "Fragmento completo de prueba.",
            }
        )
    return {"query_id": query_id, "documents": documentos, "fragments": fragmentos}


class PruebasValidadorResultados(unittest.TestCase):
    def guardar_resultados(self, carpeta, resultados):
        ruta = os.path.join(carpeta, "resultados.jsonl")
        with open(ruta, "w", encoding="utf-8") as archivo:
            for resultado in resultados:
                archivo.write(json.dumps(resultado, ensure_ascii=False) + "\n")
        return ruta

    def test_acepta_esquema_completo(self):
        with tempfile.TemporaryDirectory() as carpeta:
            resultados = [crear_resultado("q" + str(i).zfill(3)) for i in range(1, 51)]
            ruta = self.guardar_resultados(carpeta, resultados)
            reporte = validar_resultados(ruta)
            self.assertTrue(reporte["valido"])

    def test_rechaza_cantidad_incorrecta(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = self.guardar_resultados(carpeta, [crear_resultado("q001")])
            reporte = validar_resultados(ruta)
            self.assertFalse(reporte["valido"])

    def test_rechaza_fragmento_largo(self):
        with tempfile.TemporaryDirectory() as carpeta:
            resultados = [crear_resultado("q" + str(i).zfill(3)) for i in range(1, 51)]
            resultados[0]["fragments"][0]["text"] = "palabra " * 251
            ruta = self.guardar_resultados(carpeta, resultados)
            reporte = validar_resultados(ruta)
            self.assertTrue(any("250 palabras" in e for e in reporte["errores"]))

    def test_rechaza_elemento_sin_estructura(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = self.guardar_resultados(carpeta, ["resultado incorrecto"])
            reporte = validar_resultados(ruta, total_consultas=1)
            self.assertFalse(reporte["valido"])


if __name__ == "__main__":
    unittest.main()
