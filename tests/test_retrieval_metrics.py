"""Pruebas de NDCG@10 y F1@3."""

import os
import sys
import unittest


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src", "evaluation"))

from retrieval_metrics import calcular_f1_documentos, calcular_ndcg


class PruebasMetricas(unittest.TestCase):
    def test_ndcg_perfecto_es_uno(self):
        relevancias = [3, 2, 1, 0]
        self.assertAlmostEqual(calcular_ndcg(relevancias, relevancias), 1.0)

    def test_ndcg_empeora_con_orden_incorrecto(self):
        ideal = [3, 2, 1]
        obtenido = [1, 2, 3]
        self.assertLess(calcular_ndcg(obtenido, ideal), 1.0)

    def test_f1_perfecto_es_uno(self):
        metrica = calcular_f1_documentos(["d1", "d2", "d3"], ["d1", "d2", "d3"])
        self.assertAlmostEqual(metrica["f1_3"], 1.0)

    def test_f1_sin_aciertos_es_cero(self):
        metrica = calcular_f1_documentos(["d1", "d2", "d3"], ["d4"])
        self.assertEqual(metrica["f1_3"], 0.0)


if __name__ == "__main__":
    unittest.main()
