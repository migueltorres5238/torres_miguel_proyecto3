"""
Proyecto 2 - Programacion III
Alumno: Miguel Angel Torres Monroy
Archivo: main.py
Menu principal para agregar conexiones y calcular rutas con Dijkstra.
"""

from io_handler import cargar_grafo, guardar_conexion


def pedir_nodo(mensaje: str) -> str:
    """Pide el nombre de un nodo hasta que no este vacio."""
    while True:
        nombre = input(mensaje).strip().upper()
        if nombre == "":
            print("Error: el nombre no puede ir vacio.")
        else:
            return nombre


def pedir_peso() -> float:
    """Pide el peso hasta que sea un numero mayor a 0."""
    while True:
        try:
            peso = float(input("Peso (minutos): "))
            if peso <= 0:
                raise ValueError("el peso debe ser mayor a 0")
            return peso
        except ValueError as error:
            print("Error:", error, "- intenta de nuevo.")


def agregar_conexion() -> None:
    """Pide origen, destino y peso, y lo guarda en el CSV."""
    origen = pedir_nodo("Nodo origen: ")
    destino = pedir_nodo("Nodo destino: ")
    peso = pedir_peso()

    try:
        guardar_conexion(origen, destino, peso)
        print("Conexion guardada:", origen, "-", destino, "=", peso)
    except PermissionError:
        print("Error: no se tiene permiso para escribir el archivo.")


def calcular_ruta() -> None:
    """Carga el grafo desde el CSV y ejecuta Dijkstra."""
    grafo = cargar_grafo()

    if len(grafo.nodos) == 0:
        print("No hay nodos cargados.")
        return

    print("Nodos disponibles:", ", ".join(grafo.nodos))
    inicio = pedir_nodo("Nodo de inicio: ")
    destino = pedir_nodo("Nodo de destino: ")

    if inicio not in grafo.nodos or destino not in grafo.nodos:
        print("Error: uno de los nodos no existe.")
        return

    costo, ruta = grafo.dijkstra(inicio, destino)

    if costo is None:
        print("No hay ruta entre", inicio, "y", destino)
    else:
        print("Ruta mas corta:", " -> ".join(ruta))
        print("Peso total:", costo)


def main() -> None:
    """Muestra el menu hasta que el usuario elija salir."""
    while True:
        print("\n--- RED DE TRANSPORTE ---")
        print("1. Agregar conexion")
        print("2. Calcular ruta mas corta")
        print("3. Salir")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            agregar_conexion()
        elif opcion == "2":
            calcular_ruta()
        elif opcion == "3":
            print("Adios.")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()
