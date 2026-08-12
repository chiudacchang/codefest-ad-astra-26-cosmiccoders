# Avance 04 - Control de calidad, robustez y reproducibilidad

## Objetivo

Comprobar el formato final, medir recursos y revisar que el repositorio contenga
la documentación, dependencias y entregables esperados.

## Herramientas

- `results_validator.py`: aplica el contrato oficial de 50 consultas, 3
  documentos, 10 fragmentos, ranks consecutivos y máximo 250 palabras.
- `performance_monitor.py`: mide duración y pico de memoria de una función.
- `incident_manager.py`: registra un error con pasos para reproducirlo.
- `project_audit.py`: revisa dependencias, README, entregables y archivos
  potencialmente sensibles.
- `run_quality_suite.py`: coordina las revisiones disponibles.

## Conceptos utilizados

Modularización, validación de estructuras, funciones como parámetros, medición
de tiempo, memoria, archivos CSV y JSON, recorrido de carpetas y control de
excepciones.

## Sustentación corta

> La suite no supone que el pipeline está listo. Ejecuta los controles que
> tienen insumos y registra los demás como pendientes. Esto evita confundir una
> prueba no ejecutada con una prueba aprobada. Los incidentes incluyen pasos de
> reproducción para que otro integrante pueda confirmar y resolver el error.
