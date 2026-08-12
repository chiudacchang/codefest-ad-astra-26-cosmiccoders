# Avance 02 - Calidad de chunks

## Objetivo

Detectar automáticamente chunks vacíos, sin trazabilidad, duplicados, demasiado
cortos, superiores al límite de salida o posiblemente cortados. Además, producir
una muestra reproducible para revisión manual.

## Funcionamiento

`chunk_quality.py` carga archivos `.json` y `.jsonl`. Acepta `texto` o `text`
para facilitar la integración con el módulo del equipo. Por cada chunk revisa:

- presencia de `chunk_id` y `doc_id`;
- texto no vacío;
- identificadores duplicados;
- textos duplicados;
- longitud mínima y máxima;
- terminación con un signo compatible con el final de una oración.

Los campos faltantes y chunks vacíos son errores. Las longitudes y la regla de
completitud son advertencias, porque requieren interpretación humana.

## Conceptos utilizados

Funciones, listas, diccionarios, conjuntos, ciclos, condicionales, lectura de
JSON, manejo de errores, contadores y selección aleatoria con semilla.

## Sustentación corta

> Separé errores de advertencias porque una regla automática no comprende por
> completo el lenguaje. Un chunk vacío o sin identificador sí es objetivamente
> inválido; una oración sin punto final solo es sospechosa. La muestra usa una
> semilla fija para que el equipo pueda repetir exactamente la misma revisión.
