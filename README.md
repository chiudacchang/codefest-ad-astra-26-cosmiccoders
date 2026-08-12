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
