"""Auditoría de estructura, documentación, dependencias y entregables."""

import importlib.metadata
import json
import os
import sys


ENTREGABLES_FINALES = [
    "resultados.jsonl",
    "generador.py",
    "informe_tecnico.pdf",
    "base_vectorial",
]


def leer_requirements(ruta_requirements):
    """Obtiene los nombres de paquetes declarados en requirements.txt."""
    paquetes = []
    if not os.path.isfile(ruta_requirements):
        return paquetes

    with open(ruta_requirements, "r", encoding="utf-8-sig") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea != "" and not linea.startswith("#"):
                nombre = linea.split("==")[0].split(">=")[0].strip()
                paquetes.append(nombre)
    return paquetes


def revisar_dependencias(ruta_requirements):
    """Comprueba qué dependencias declaradas están instaladas."""
    resultados = []
    for paquete in leer_requirements(ruta_requirements):
        try:
            version = importlib.metadata.version(paquete)
            resultados.append(
                {"paquete": paquete, "instalado": True, "version": version}
            )
        except importlib.metadata.PackageNotFoundError:
            resultados.append(
                {"paquete": paquete, "instalado": False, "version": ""}
            )
    return resultados


def revisar_entregables(raiz):
    """Comprueba la presencia de los cuatro componentes obligatorios."""
    resultados = []
    for nombre in ENTREGABLES_FINALES:
        ruta = os.path.join(raiz, nombre)
        resultados.append(
            {"entregable": nombre, "existe": os.path.exists(ruta), "ruta": ruta}
        )
    return resultados


def revisar_documentacion(raiz):
    """Comprueba elementos mínimos del README y archivos de apoyo."""
    hallazgos = []
    ruta_readme = os.path.join(raiz, "README.md")
    if not os.path.isfile(ruta_readme):
        return ["Falta README.md"]

    with open(ruta_readme, "r", encoding="utf-8") as archivo:
        texto = archivo.read().lower()

    temas = {
        "descripción del proyecto": ("codefest", "base de conocimiento"),
        "instalación": ("instalación", "install"),
        "ejecución": ("ejecución", "ejecutar"),
        "pruebas": ("pruebas", "unittest"),
        "estructura": ("estructura", "src/"),
    }
    for tema, palabras in temas.items():
        encontrado = False
        for palabra in palabras:
            if palabra in texto:
                encontrado = True
        if not encontrado:
            hallazgos.append("El README no explica: " + tema)
    return hallazgos


def buscar_archivos_sensibles(raiz):
    """Busca nombres de archivos que podrían contener credenciales."""
    sensibles = []
    nombres = (".env", "credentials.json", "secrets.json", "token.txt")
    for carpeta_actual, carpetas, archivos in os.walk(raiz):
        carpetas[:] = [c for c in carpetas if c not in (".git", ".venv", "venv")]
        for nombre in archivos:
            if nombre.lower() in nombres:
                sensibles.append(os.path.relpath(os.path.join(carpeta_actual, nombre), raiz))
    return sensibles


def auditar_proyecto(raiz="."):
    """Construye el reporte general de auditoría del proyecto."""
    dependencias = revisar_dependencias(os.path.join(raiz, "requirements.txt"))
    faltantes = [d["paquete"] for d in dependencias if not d["instalado"]]
    entregables = revisar_entregables(raiz)
    pendientes = [e["entregable"] for e in entregables if not e["existe"]]
    documentacion = revisar_documentacion(raiz)
    sensibles = buscar_archivos_sensibles(raiz)

    return {
        "version_python": sys.version.split()[0],
        "dependencias": dependencias,
        "dependencias_faltantes": faltantes,
        "entregables": entregables,
        "entregables_pendientes": pendientes,
        "hallazgos_documentacion": documentacion,
        "archivos_sensibles": sensibles,
        "listo_para_entrega": not pendientes
        and not faltantes
        and not documentacion
        and not sensibles,
    }


def main():
    """Ejecuta la auditoría y guarda un reporte JSON."""
    reporte = auditar_proyecto(".")
    os.makedirs("results", exist_ok=True)
    with open("results/auditoria_proyecto.json", "w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, ensure_ascii=False, indent=4)
    print("Entregables pendientes:", len(reporte["entregables_pendientes"]))
    print("Dependencias faltantes:", len(reporte["dependencias_faltantes"]))
    print("Hallazgos documentales:", len(reporte["hallazgos_documentacion"]))


if __name__ == "__main__":
    main()
