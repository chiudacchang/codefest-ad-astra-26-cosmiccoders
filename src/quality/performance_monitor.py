"""Medición sencilla de tiempo y memoria para pruebas de robustez."""

import time
import tracemalloc


def medir_funcion(funcion, argumento):
    """Ejecuta una función con un argumento y mide tiempo y memoria."""
    tracemalloc.start()
    inicio = time.perf_counter()

    resultado = funcion(argumento)

    fin = time.perf_counter()
    memoria_actual, memoria_maxima = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "resultado": resultado,
        "duracion_segundos": round(fin - inicio, 6),
        "memoria_actual_mb": round(memoria_actual / (1024 * 1024), 4),
        "memoria_maxima_mb": round(memoria_maxima / (1024 * 1024), 4),
    }
