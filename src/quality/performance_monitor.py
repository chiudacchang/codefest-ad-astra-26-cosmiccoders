"""Medición sencilla de tiempo y memoria para pruebas de robustez."""

import time
import tracemalloc


def medir_funcion(funcion, *argumentos, **argumentos_con_nombre):
    """Ejecuta una función y retorna resultado, tiempo y pico de memoria."""
    tracemalloc.start()
    inicio = time.perf_counter()

    resultado = funcion(*argumentos, **argumentos_con_nombre)

    fin = time.perf_counter()
    memoria_actual, memoria_maxima = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "resultado": resultado,
        "duracion_segundos": round(fin - inicio, 6),
        "memoria_actual_mb": round(memoria_actual / (1024 * 1024), 4),
        "memoria_maxima_mb": round(memoria_maxima / (1024 * 1024), 4),
    }
