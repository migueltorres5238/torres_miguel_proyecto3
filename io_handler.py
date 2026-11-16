"""
Proyecto 2 - Programacion III
Alumno: Miguel Angel Torres Monroy
Archivo: io_handler.py
Funciones para escribir y leer el archivo nodos.csv.
"""

import csv
import os

from grafo import Grafo

ARCHIVO = "nodos.csv"


def guardar_conexion(origen: str, destino: str, peso: float) -> None:
    """Guarda una conexion al final del CSV (modo append)."""
    # Si el archivo no existe se le pone el encabezado primero
    existe = os.path.exists(ARCHIVO)

    with open(ARCHIVO, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if not existe:
            escritor.writerow(["Origen", "Destino", "Peso"])
        escritor.writerow([origen, destino, peso])


def cargar_grafo() -> Grafo:
    """Lee el CSV fila por fila y arma el grafo. Salta las filas malas."""
    grafo = Grafo()

    try:
        with open(ARCHIVO, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                try:
                    origen = fila["Origen"]
                    destino = fila["Destino"]
                    peso = float(fila["Peso"])

                    if not origen or not destino:
                        raise ValueError("falta un nodo")
                    if peso <= 0:
                        raise ValueError("el peso debe ser mayor a 0")

                    grafo.agregar_arista(origen, destino, peso)

                except KeyError as error:
                    print("Falta el encabezado", error, "en el CSV")
                except (ValueError, TypeError) as error:
                    print("Fila omitida", fila, "->", error)

    except FileNotFoundError:
        print("No existe", ARCHIVO, "todavia, agrega conexiones primero.")

    return grafo
