# CODEFEST AD ASTRA 2026 - Cosmic Coders

Implementación de una base de conocimiento vectorial con FAISS para el análisis
de fenómenos aeroespaciales y estratégicos. Proyecto para la Etapa 1 del
CODEFEST AD ASTRA 2026.

## Avance del integrante 4

El primer avance incluye herramientas para validar el corpus documental y
generar estadísticas básicas antes de iniciar el procesamiento de los archivos.

### Instalación

Desde la carpeta principal del repositorio:

```bash
python -m pip install -r requirements.txt
```

### Ejecución

1. Guardar los documentos del corpus dentro de `data/raw/`.
2. Ejecutar:

```bash
python src/utils/run_validation.py
```

Los resultados se guardan en:

- `results/estadisticas.json`: resumen general y detalle por archivo.
- `results/reporte_errores.json`: archivos rechazados y motivo del rechazo.

Para analizar otra carpeta se puede escribir su ruta después del programa:

```bash
python src/utils/run_validation.py ruta/de/la/carpeta
```

### Pruebas

```bash
python -m unittest discover -s tests -v
```

La explicación detallada del avance y las preguntas de preparación para la
sustentación están en
[`docs/avances/avance_01_validacion_corpus.md`](docs/avances/avance_01_validacion_corpus.md).

## Suite de calidad del integrante 4

La suite revisa los componentes que ya estén disponibles y marca los demás como
pendientes, sin inventar resultados:

```bash
python src/quality/run_quality_suite.py data/chunks resultados.jsonl
```

También es posible ejecutar cada control por separado:

```bash
python src/quality/chunk_quality.py data/chunks
python src/quality/results_validator.py resultados.jsonl
python src/quality/project_audit.py
```

Para calcular las métricas cuando existan juicios de relevancia:

```bash
python src/evaluation/retrieval_metrics.py resultados.jsonl juicios.jsonl
```

Documentos principales del integrante 4:

- [`docs/PLAN_CALIDAD_INTEGRANTE_4.md`](docs/PLAN_CALIDAD_INTEGRANTE_4.md)
- [`docs/GUIA_SUSTENTACION_INTEGRANTE_4.md`](docs/GUIA_SUSTENTACION_INTEGRANTE_4.md)
- [`docs/RETROSPECTIVA.md`](docs/RETROSPECTIVA.md)
