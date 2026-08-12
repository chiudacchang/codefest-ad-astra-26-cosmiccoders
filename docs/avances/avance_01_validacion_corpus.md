# Avance 01 - Validación inicial del corpus

## Objetivo

Construir una herramienta que revise los documentos antes de que el equipo los
use para crear fragmentos, embeddings e índices FAISS. Esta revisión temprana
evita que un archivo vacío, corrupto o mal codificado detenga el pipeline.

## Qué se hizo

Se organizaron las responsabilidades en tres programas:

1. `corpus_validator.py`: determina si un archivo puede procesarse.
2. `corpus_stats.py`: extrae texto y calcula estadísticas básicas.
3. `run_validation.py`: recorre el corpus, llama a los otros programas y guarda
   los reportes.

También se agregaron pruebas automáticas, instrucciones de ejecución y reglas
para evitar que el corpus y los resultados generados se suban por accidente a
GitHub.

## Cómo funciona el código

### 1. Validación

La función `archivo_valido` recibe la ruta de un archivo y retorna una tupla:

```python
(True, "Archivo de texto válido")
```

El primer valor indica si el archivo fue aceptado. El segundo explica el
resultado. La función comprueba primero que la ruta exista, que sea un archivo y
que su tamaño sea mayor que cero. Después selecciona una validación según la
extensión:

- Los archivos de texto se abren usando UTF-8.
- Los JSON se leen con `json.load` para comprobar su estructura.
- Los PDF se abren con `PdfReader` y deben contener al menos una página.
- Los XLSX se verifican como archivos ZIP, porque internamente usan ese formato.
- Los demás formatos se aceptan si no están vacíos, pero se marcan para revisión
  posterior.

### 2. Estadísticas

`extraer_estadisticas` devuelve un diccionario con formato, cantidad de
caracteres, cantidad de palabras e idioma. Para contar palabras se usa
`texto.split()`, que divide el texto por espacios. El idioma se detecta con la
librería `langdetect`; si no hay texto o la detección falla, se registra como
`desconocido`.

### 3. Coordinación

`procesar_corpus` usa `os.walk` para recorrer la carpeta y sus subcarpetas. Los
archivos técnicos ocultos, como `.gitkeep`, se ignoran. Cada archivo válido se
agrega a una lista de detalles y cada archivo rechazado se agrega a una lista de
errores. Los contadores por formato e idioma se guardan en diccionarios.

Al terminar se crean dos archivos JSON:

- `estadisticas.json`, con el resumen y el detalle completo.
- `reporte_errores.json`, con los documentos que requieren atención.

## Conceptos de Python implementados

- Variables para almacenar rutas, textos y contadores.
- Funciones para dividir el problema en tareas pequeñas.
- Condicionales `if`, `elif` y `else` para tomar decisiones.
- Ciclos `for` para recorrer carpetas, archivos y páginas.
- Listas para almacenar resultados y errores.
- Diccionarios para representar estadísticas y contadores.
- Tuplas para retornar el estado y el mensaje de validación.
- Manejo de archivos con `with open`.
- Manejo de excepciones con `try` y `except`.
- Uso de librerías mediante `import`.
- Pruebas con `unittest` para comprobar resultados esperados.

## Decisiones y justificación

### Separar el programa en tres archivos

Cada archivo tiene una responsabilidad clara. Esto permite encontrar errores
con mayor facilidad y probar una función sin ejecutar todo el proceso.

### Usar JSON para los reportes

JSON representa listas y diccionarios de Python de forma directa. Además, otros
módulos del proyecto pueden leer los resultados posteriormente.

### No subir `data/raw`

El corpus puede ser grande y puede contener material que no debe duplicarse en
GitHub. Por eso `.gitignore` conserva solamente la carpeta vacía.

### Marcar formatos pendientes

En este primer avance no se extrae texto de imágenes, PBF o XLSX. El validador
no afirma que su contenido sea correcto: indica que necesitan una revisión
posterior. Esto evita presentar una comprobación incompleta como definitiva.

## Pruebas realizadas

Las pruebas comprueban siete situaciones:

1. Un archivo vacío debe ser rechazado.
2. Un texto UTF-8 válido debe ser aceptado.
3. Un JSON con estructura incorrecta debe ser rechazado.
4. Un PDF con una página debe ser aceptado.
5. Un archivo que aparenta ser PDF, pero está corrupto, debe ser rechazado.
6. El proceso completo debe generar los dos reportes.
7. Los archivos técnicos ocultos de Git no deben contarse como documentos.

## Limitaciones conocidas y próximo paso

- La detección de idioma depende de la cantidad y calidad del texto.
- Un PDF escaneado puede ser válido, pero no producir texto sin aplicar OCR.
- Las imágenes y los archivos PBF todavía no tienen validación especializada.
- La comprobación de XLSX es estructural y no analiza sus hojas.

El próximo avance debe probar el programa con una muestra real del corpus y
agregar validaciones especializadas según los formatos encontrados.

## Preguntas para la sustentación

### ¿Por qué se retorna una tupla desde `archivo_valido`?

Porque se necesitan dos resultados: un booleano que indique si el archivo fue
aceptado y un texto que explique la decisión.

### ¿Por qué se usa `try` y `except`?

Porque abrir un documento puede fallar. La excepción permite registrar el error
y continuar con los demás archivos en lugar de detener todo el programa.

### ¿Qué diferencia hay entre una lista y un diccionario en este programa?

La lista guarda varios elementos del mismo tipo, como todos los archivos
rechazados. El diccionario relaciona claves con valores, como el nombre de una
estadística y su resultado.

### ¿Por qué se usa `os.walk` y no solamente `os.listdir`?

`os.listdir` revisa un solo nivel. `os.walk` también recorre las subcarpetas, lo
que permite validar un corpus organizado por fuentes o formatos.

### ¿Por qué las pruebas crean carpetas temporales?

Para probar el programa sin modificar el corpus real. La carpeta y sus archivos
se eliminan automáticamente al finalizar cada prueba.
