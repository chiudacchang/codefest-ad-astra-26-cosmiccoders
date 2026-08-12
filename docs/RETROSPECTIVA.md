# Retrospectiva del proyecto - Integrante 4

Este documento se completa únicamente con evidencia real. Los campos pendientes
no deben reemplazarse con resultados estimados.

## Logros comprobados

- Se construyó un validador inicial del corpus con reportes de errores y
  estadísticas.
- Se agregó una evaluación automática de chunks con muestra reproducible para
  revisión manual.
- Se codificó la validación estricta del esquema oficial de
  `resultados.jsonl`.
- Se implementaron NDCG@10 y F1@3 de acuerdo con la especificación del reto.
- Se crearon registros uniformes para experimentos e incidentes.
- Se agregó auditoría de dependencias, documentación, entregables y archivos
  sensibles.
- Se añadieron pruebas automáticas para las herramientas de calidad.

## Dificultades enfrentadas

- Los módulos del equipo se desarrollan en ramas diferentes y sus interfaces
  cambian durante la integración.
- El corpus, los chunks y la recuperación completa todavía no están disponibles
  simultáneamente; por eso algunas pruebas permanecen pendientes.
- `requirements.txt` estaba guardado en UTF-16 y fue necesario normalizarlo a
  UTF-8 para facilitar instalaciones reproducibles.

## Decisiones técnicas

- Las herramientas aceptan archivos JSON y JSON Lines para integrarse con los
  formatos del reto.
- Los reportes se guardan en JSON o CSV porque ambos formatos son legibles y
  fáciles de procesar con Python.
- Los límites estrictos de 3 documentos, 10 fragmentos, 250 palabras y 50
  consultas se validan antes de entregar.
- Las reglas lingüísticas automáticas se reportan como advertencias, ya que no
  reemplazan la revisión humana.
- La suite no inventa resultados: marca una prueba como pendiente cuando falta
  su insumo.

## Experimentos exitosos

Pendiente: registrar aquí las configuraciones que hayan sido ejecutadas y
comparadas en `registro_experimentos.csv`.

## Errores y soluciones

Pendiente: resumir los incidentes reales registrados durante la integración.

## Recomendaciones para la Etapa 2

- Conservar los reportes de calidad como controles previos a cada despliegue.
- Versionar las configuraciones de encoder, chunking e índice junto con los
  resultados que producen.
- Mantener consultas de regresión para detectar disminuciones en recuperación.
- No presentar una mejora como válida sin comparar métricas, tiempo y memoria.

## Información pendiente para el cierre

- Estadísticas reales del corpus completo.
- Distribución y hallazgos reales de chunks.
- Configuración ganadora y métricas reales.
- Consumo real de memoria y tiempo del pipeline completo.
- Incidentes resueltos y lecciones del equipo.
