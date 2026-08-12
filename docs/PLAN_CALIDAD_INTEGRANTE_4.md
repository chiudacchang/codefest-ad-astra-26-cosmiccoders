# Plan de calidad - Integrante 4

## Propósito

Este documento relaciona las responsabilidades de Chiu con herramientas,
evidencias y condiciones de cierre. Un punto solo se marca como terminado cuando
existen insumos reales y un reporte generado por el programa.

## Matriz de responsabilidades

| Responsabilidad | Herramienta o evidencia | Estado técnico |
|---|---|---|
| Validación del corpus | `src/utils/run_validation.py` | Implementada; falta ejecutar sobre el corpus oficial |
| Estadísticas del corpus | `results/estadisticas.json` | Generación implementada; falta corpus oficial |
| Calidad de chunks | `src/quality/chunk_quality.py` | Implementada; espera salida de chunking |
| Muestra manual de chunks | `muestra_revision_manual` en el reporte | Selección reproducible implementada |
| Consultas experimentales | `docs/templates/consultas_prueba.jsonl` | Conjunto inicial creado |
| Formato de resultados | `src/quality/results_validator.py` | Validación oficial implementada |
| NDCG@10 y F1@3 | `src/evaluation/retrieval_metrics.py` | Implementadas; esperan juicios y resultados |
| Registro de experimentos | `src/evaluation/experiment_manager.py` | Implementado |
| Registro de incidentes | `src/quality/incident_manager.py` | Implementado |
| Tiempo y memoria | `src/quality/performance_monitor.py` | Implementado para funciones Python |
| Auditoría documental y de entrega | `src/quality/project_audit.py` | Implementada; se ejecuta durante el desarrollo |
| Suite funcional | `src/quality/run_quality_suite.py` | Implementada con controles condicionales |
| Reproducibilidad | `requirements.txt`, README y auditoría | Parcial hasta contar con pipeline completo |
| Retrospectiva | `docs/RETROSPECTIVA.md` | Documento vivo; cierre pendiente |
| Preparación de sustentación | `docs/GUIA_SUSTENTACION_INTEGRANTE_4.md` | Guía inicial completa; actualizar con resultados reales |

## Criterios de cierre

Antes de afirmar que la parte del integrante 4 está terminada deben cumplirse
todos estos puntos:

1. Ejecutar la validación sobre el corpus oficial y revisar los rechazados.
2. Ejecutar la calidad sobre todos los chunks y revisar manualmente la muestra.
3. Ejecutar consultas de prueba y registrar configuración, tiempo y memoria.
4. Completar juicios manuales para el conjunto experimental interno.
5. Calcular NDCG@10 y F1@3 sin errores de formato.
6. Validar las 50 líneas finales de `resultados.jsonl`.
7. Instalar el proyecto desde cero y repetir la generación de resultados.
8. Confirmar nombres y estructura de todos los entregables.
9. Revisar README, informe técnico, bibliografía y consistencia con el código.
10. Completar la retrospectiva con resultados y decisiones reales.

## Regla de evidencia

Un reporte vacío, una plantilla o una prueba pendiente no cuenta como resultado.
Las cifras que se incluyan en el informe deben proceder de archivos generados por
una ejecución identificable en el registro experimental.
