# Avance 03 - Evaluación y registro experimental

## Objetivo

Aplicar las métricas oficiales y mantener trazabilidad entre configuración,
parámetros, resultados y conclusiones.

## Métricas

`retrieval_metrics.py` implementa:

- NDCG@10 para medir el orden de los fragmentos relevantes.
- F1@3 para medir el conjunto de documentos relevantes recuperados.

La relevancia de fragmentos se compara mediante texto normalizado, no mediante
`chunk_id`, tal como exige el reto. Los juicios oficiales no son públicos; para
experimentos internos se deben crear juicios manuales usando la plantilla.

## Registro

`experiment_manager.py` almacena fecha, responsable, configuración, parámetros,
tiempo, memoria, consultas, métricas, errores, observaciones y conclusión. El
consolidado permite comparar ejecuciones y seleccionar una configuración con
evidencia.

## Conceptos utilizados

Funciones, fórmulas matemáticas, listas, conjuntos, diccionarios, CSV, JSON,
fechas, acumuladores, promedios y ordenamiento.

## Sustentación corta

> NDCG premia que los fragmentos más relevantes aparezcan primero. F1 combina
> precisión y cobertura de los tres documentos. Guardé cada experimento con sus
> parámetros para que una cifra siempre pueda reproducirse y asociarse a una
> configuración concreta.
