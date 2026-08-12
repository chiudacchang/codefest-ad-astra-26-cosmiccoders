"""Pruebas del registro experimental, incidentes y medición de rendimiento."""

import os
import sys
import tempfile
import unittest


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src", "evaluation"))
sys.path.insert(0, os.path.join(RAIZ, "src", "quality"))

from experiment_manager import crear_registro, guardar_registro, leer_registros
from incident_manager import crear_incidente, guardar_incidente
from performance_monitor import medir_funcion


class PruebasHerramientasExperimentales(unittest.TestCase):
    def test_guarda_experimento(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "experimentos.csv")
            registro = crear_registro("Chiu", "Flat", {"top_k": 10})
            guardar_registro(ruta, registro)
            self.assertEqual(len(leer_registros(ruta)), 1)

    def test_guarda_incidente(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "incidentes.csv")
            incidente = crear_incidente(
                "chunking", "media", "Chunk vacío", "Ejecutar prueba", "Texto", "Vacío"
            )
            guardar_incidente(ruta, incidente)
            self.assertTrue(os.path.isfile(ruta))

    def test_mide_funcion(self):
        medicion = medir_funcion(sum, [1, 2, 3])
        self.assertEqual(medicion["resultado"], 6)
        self.assertGreaterEqual(medicion["duracion_segundos"], 0)
        self.assertGreaterEqual(medicion["memoria_maxima_mb"], 0)


if __name__ == "__main__":
    unittest.main()
