# Guía de sustentación - Integrante 4 (Chiu)

## Regla principal

No memorices el código línea por línea. Debes poder explicar el problema, la
decisión tomada, el flujo de datos, la evidencia obtenida y las limitaciones.
Antes de presentar, ejecuta cada comando y reemplaza en esta guía los estados
pendientes por resultados reales.

## Presentación sugerida de 10 minutos

### Minuto 0 a 1 - Mi responsabilidad

> Mi rol fue ingeniería de validación y documentación. Mi objetivo no era crear
> el encoder o el índice, sino comprobar que los datos de entrada, los chunks,
> los experimentos y los entregables fueran correctos, reproducibles y
> trazables. Construí controles automáticos, registros y pruebas para detectar
> errores antes de la entrega.

### Minuto 1 a 3 - Validación del corpus

Muestra `corpus_validator.py`, `corpus_stats.py` y `run_validation.py`.

Explica este flujo:

1. Se recibe la ruta del corpus.
2. `os.walk` recorre archivos y subcarpetas.
3. `archivo_valido` comprueba existencia, tipo y tamaño.
4. Se aplica una validación según la extensión.
5. Los archivos aceptados pasan al cálculo de estadísticas.
6. Se generan `estadisticas.json` y `reporte_errores.json`.

Frase sugerida:

> Separé la validación de las estadísticas para que cada módulo tuviera una sola
> responsabilidad. Un archivo vacío, mal codificado o corrupto se registra y no
> detiene la revisión del resto del corpus.

Conceptos que debes dominar:

- `with open`: abre el archivo y garantiza su cierre.
- UTF-8: codificación usada para convertir bytes en caracteres.
- `try` y `except`: permite manejar un fallo sin detener todo el programa.
- tupla `(booleano, mensaje)`: devuelve la decisión y su explicación.
- lista: almacena varios resultados.
- diccionario: relaciona nombres de campos con valores.

### Minuto 3 a 4:30 - Calidad de chunks

Muestra `chunk_quality.py` y `calidad_chunks.json` cuando exista.

Explica:

1. Se cargan chunks desde JSON o JSON Lines.
2. Se busca el texto en `texto`, `text` o `contenido` para admitir cambios de
   interfaz durante la integración.
3. Se verifican `chunk_id`, `doc_id`, texto, duplicados y longitud.
4. Se separan errores de advertencias.
5. Se crea una muestra con semilla 42 para revisión manual reproducible.

Frase sugerida:

> Una regla automática no entiende completamente el lenguaje. Por eso un chunk
> vacío es un error, mientras que una posible oración cortada es una advertencia
> que debe confirmar una persona.

Conceptos:

- conjunto (`set`): detecta valores repetidos rápidamente;
- normalización: convierte variaciones superficiales a una forma comparable;
- semilla aleatoria: permite repetir exactamente la misma muestra;
- parámetro: permite cambiar límites sin reescribir la función.

### Minuto 4:30 a 6:30 - Evaluación experimental

Muestra `retrieval_metrics.py`, `experiment_manager.py` y las plantillas.

#### NDCG@10

> NDCG mide si los fragmentos más relevantes aparecen en las primeras
> posiciones. Cada relevancia se divide por un logaritmo que aumenta con la
> posición, así que un resultado relevante vale más arriba que abajo. El DCG
> obtenido se divide por el DCG ideal y produce un valor entre cero y uno.

Pasos de la función:

1. Recorre hasta diez relevancias.
2. Calcula `relevancia / log2(posición + 1)` usando índices matemáticos.
3. Ordena las relevancias para obtener el ranking ideal.
4. Divide DCG por IDCG.

#### F1@3

> F1@3 mide los tres documentos como conjunto, sin importar el orden. Precisión
> indica cuántos de los tres entregados son correctos. Recall indica cuántos de
> los relevantes disponibles se recuperaron. F1 combina ambas medidas.

Pasos:

1. Convierte documentos obtenidos y relevantes en conjuntos.
2. Calcula la intersección para contar aciertos.
3. Calcula precisión y recall.
4. Calcula la media armónica F1.

#### Registro experimental

> Cada ejecución queda asociada a fecha, responsable, configuración, parámetros,
> tiempo, memoria, métricas, errores y conclusión. Así puedo justificar por qué
> una configuración fue elegida y repetirla después.

Conceptos:

- `math.log2`: logaritmo base dos;
- acumulador: variable que suma resultados dentro de un ciclo;
- intersección de conjuntos: elementos presentes en ambos conjuntos;
- CSV: tabla de texto para experimentos;
- JSON: estructura para reportes y parámetros;
- promedio: suma dividida por cantidad de observaciones.

### Minuto 6:30 a 8 - Formato final y robustez

Muestra `results_validator.py`, `performance_monitor.py` y
`incident_manager.py`.

Contrato oficial que debes saber sin leer:

- 50 líneas en orden `q001` a `q050`;
- cada línea es un objeto JSON independiente;
- exactamente 3 documentos;
- exactamente 10 fragmentos;
- ranks consecutivos;
- cada fragmento tiene `chunk_id`, `doc_id` y `text`;
- máximo 250 palabras por fragmento.

Frase sugerida:

> Codifiqué el contrato oficial como validaciones automáticas. Esto reduce el
> riesgo de perder puntos por un error de formato aunque la recuperación sea
> buena.

Medición:

> `performance_monitor.py` toma el tiempo con `perf_counter` y el pico de memoria
> con `tracemalloc`. La función que se mide se recibe como parámetro, por lo que
> el mismo instrumento sirve para chunking, recuperación o validación.

Incidentes:

> Un incidente registra pasos de reproducción, resultado esperado, resultado
> obtenido, severidad, estado y solución. Esto convierte un comentario informal
> en un error verificable por cualquier integrante.

### Minuto 8 a 9 - Reproducibilidad y auditoría

Muestra `project_audit.py`, `requirements.txt` y el README.

Explica:

1. `requirements.txt` fija versiones de dependencias.
2. La auditoría comprueba si están instaladas.
3. Revisa los cuatro entregables obligatorios.
4. Comprueba temas mínimos del README.
5. Busca nombres comunes de archivos con secretos.
6. No declara el proyecto listo si existe algún pendiente.

Frase sugerida:

> Reproducibilidad significa que otra persona puede instalar las dependencias,
> ejecutar el proyecto y obtener los resultados sin conocer mi computador. La
> auditoría hace visibles los faltantes en lugar de depender de una revisión de
> memoria.

### Minuto 9 a 10 - Evidencia, límites y cierre

> Las pruebas automáticas de mis herramientas están aprobadas. Las pruebas sobre
> corpus, chunks, índice y resultados finales solo se marcarán como terminadas
> cuando existan esos insumos reales. No reporto métricas estimadas. La principal
> recomendación es conservar configuración, resultados y reporte de calidad como
> una misma unidad experimental.

Termina mostrando el plan de calidad y la retrospectiva.

## Demostración paso a paso

Ejecuta desde la raíz del repositorio.

### 1. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

Explicación: `pip` lee cada paquete y versión, lo descarga y lo instala en el
entorno activo.

### 2. Ejecutar pruebas automáticas

```bash
python -m unittest discover -s tests -v
```

Explicación: `discover` busca archivos que empiecen con `test`, ejecuta cada caso
y muestra `ok` o el error encontrado.

### 3. Validar el corpus

```bash
python src/utils/run_validation.py RUTA_DEL_CORPUS
```

Debes mostrar los totales reales de válidos, rechazados, formatos e idiomas.

### 4. Validar chunks

```bash
python src/quality/chunk_quality.py data/chunks
```

Muestra promedio, mínimo, máximo, errores, advertencias y muestra manual.

### 5. Ejecutar la suite

```bash
python src/quality/run_quality_suite.py data/chunks resultados.jsonl
```

Explica cualquier control pendiente. Pendiente no significa aprobado ni fallido;
significa que no existía el insumo.

### 6. Validar la entrega

```bash
python src/quality/results_validator.py resultados.jsonl
```

No se debe entregar mientras `valido` sea `false`.

### 7. Calcular métricas internas

```bash
python src/evaluation/retrieval_metrics.py resultados_prueba.jsonl juicios.jsonl
```

Solo se ejecuta después de completar juicios manuales. Los juicios oficiales no
son públicos durante el reto.

## Preguntas probables y respuestas

### ¿Por qué usaste JSON Lines?

Porque el formato oficial exige un objeto JSON independiente por consulta. Se
puede procesar línea por línea sin cargar todo el archivo.

### ¿Cuál es la diferencia entre `doc_id` y `chunk_id`?

`doc_id` identifica el archivo original. `chunk_id` identifica una parte de ese
documento. Varios chunks pueden compartir el mismo `doc_id`.

### ¿Por qué NDCG usa el texto y no `chunk_id`?

Cada equipo crea chunks diferentes. El identificador es interno y no coincide
con un ground truth común; el contenido textual es la evidencia evaluada.

### ¿Por qué F1 no considera el orden?

La especificación define F1@3 como métrica de conjunto. Solo importa cuáles de
los tres documentos son relevantes.

### ¿Qué pasa si IDCG es cero?

No hay ganancia ideal disponible. Para evitar división por cero, la función
retorna cero.

### ¿Por qué no aceptas 251 palabras?

El contrato oficial define máximo 250. El validador debe ser estricto porque la
evaluación automática puede penalizar o descartar el resultado.

### ¿La regla del punto final garantiza completitud lingüística?

No. Es una heurística para señalar sospechas. Por eso genera una advertencia y
se complementa con revisión manual.

### ¿Por qué usaste una semilla aleatoria?

Para seleccionar una muestra sin sesgo manual y poder repetir exactamente la
misma selección.

### ¿Cuál es la diferencia entre error y excepción?

Un error de calidad es una condición encontrada en los datos. Una excepción es
un evento de Python que interrumpe una operación, como intentar leer un archivo
corrupto. `try/except` transforma la excepción en un hallazgo registrable.

### ¿Qué significa reproducible?

Que otra persona puede preparar un entorno limpio, instalar las versiones
declaradas, ejecutar los mismos comandos y obtener resultados consistentes.

### ¿Qué harías si una configuración mejora NDCG pero consume mucha memoria?

Compararía métricas, tiempo y memoria en el registro experimental. La decisión
debe equilibrar calidad y estabilidad según los recursos disponibles.

### ¿Qué limitaciones tiene tu trabajo?

La detección de idioma depende del texto extraído; los PDF escaneados pueden
necesitar OCR; la completitud lingüística automática es aproximada; y las
métricas finales requieren resultados y juicios reales.

## Conceptos de Python usados

### Variables

Guardan valores que cambian durante el programa: rutas, contadores, textos y
resultados.

### Funciones

Dividen el problema en operaciones pequeñas que pueden probarse y reutilizarse.

### Parámetros y retorno

Los parámetros entregan datos a una función. `return` devuelve el resultado al
programa que la llamó.

### Condicionales

`if`, `elif` y `else` seleccionan una acción según una condición.

### Ciclos

`for` recorre archivos, chunks, consultas y resultados. `os.walk` permite
recorrer una jerarquía de carpetas.

### Listas

Mantienen colecciones ordenadas, como detalles o hallazgos.

### Diccionarios

Representan objetos con campos nombrados, como un reporte o un fragmento.

### Tuplas

Agrupan valores que se retornan juntos, como `(válido, mensaje)`.

### Conjuntos

Mantienen elementos únicos y permiten detectar duplicados o calcular
intersecciones.

### Archivos y codificación

`open` permite leer o escribir. UTF-8 representa caracteres de varios idiomas.
El modo `newline=""` evita líneas adicionales al escribir CSV en Windows.

### Excepciones

`try/except` maneja fallos esperables, permite continuar y registrar la causa.

### Módulos y librerías

`import` reutiliza funciones disponibles. Se usaron módulos estándar y librerías
especializadas para PDF e idioma.

### Pruebas unitarias

Cada prueba prepara una entrada, ejecuta una función y compara el resultado con
lo esperado mediante afirmaciones como `assertEqual`.

Los archivos de prueba usan `unittest.TestCase`. Es una estructura proporcionada
por la librería `unittest` para agrupar casos relacionados. No se usa orientación
a objetos en los programas del proyecto; la clase aparece únicamente porque es
la forma estándar en que esta librería organiza sus pruebas.

### Funciones recibidas como parámetros

`medir_funcion` recibe otra función y un argumento. Esto permite aplicar el mismo
cronómetro a diferentes procesos. La función recibida no se ejecuta al enviarla;
se ejecuta dentro del medidor mediante `funcion(argumento)`.

### Trazabilidad

No es una instrucción específica de Python: es una práctica de ingeniería. Cada
resultado debe relacionarse con sus datos, configuración, fecha y conclusión.

## Lista final antes de presentar

- [ ] Puedo explicar cada archivo sin leer esta guía.
- [ ] Ejecuté las pruebas y conozco el número actualizado de casos aprobados.
- [ ] Reemplacé todos los pendientes por evidencia o expliqué por qué siguen pendientes.
- [ ] Conozco las estadísticas reales del corpus y chunks.
- [ ] Puedo explicar NDCG@10 y F1@3 con un ejemplo pequeño.
- [ ] Puedo recitar el contrato de `resultados.jsonl`.
- [ ] Tengo al menos un experimento y un incidente real documentados.
- [ ] Probé instalación y ejecución en un entorno limpio.
- [ ] Verifiqué los cuatro entregables finales.
- [ ] Revisé que la retrospectiva no contenga datos inventados.
