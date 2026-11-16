"""
Proyecto 2 - Programacion III
Alumno: Miguel Angel Torres Monroy
Archivo: grafo.py
Clases Nodo y Grafo con el algoritmo de Dijkstra (Unidad 1).
"""

from typing import Dict, List, Optional, Tuple


class Nodo:
    """Guarda una estacion y sus vecinos con el peso de cada conexion."""

    def __init__(self, nombre: str) -> None:
        """Crea el nodo con su nombre y sin vecinos."""
        self.nombre = nombre
        self.vecinos: Dict[str, float] = {}

    def agregar_vecino(self, vecino: str, peso: float) -> None:
        """Agrega un vecino con su peso."""
        self.vecinos[vecino] = peso


class Grafo:
    """Grafo no dirigido donde se guardan todos los nodos."""

    def __init__(self) -> None:
        """Crea el grafo vacio."""
        self.nodos: Dict[str, Nodo] = {}

    def agregar_nodo(self, nombre: str) -> None:
        """Agrega un nodo si todavia no existe."""
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

    def agregar_arista(self, origen: str, destino: str, peso: float) -> None:
        """Conecta dos nodos en los dos sentidos."""
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.nodos[origen].agregar_vecino(destino, peso)
        self.nodos[destino].agregar_vecino(origen, peso)

    def dijkstra(
        self, inicio: str, destino: str
    ) -> Tuple[Optional[float], List[str]]:
        """Regresa el costo y la ruta mas corta. Si no hay ruta da None."""
        distancias: Dict[str, float] = {}
        anteriores: Dict[str, Optional[str]] = {}
        visitados = set()

        for nombre in self.nodos:
            distancias[nombre] = float("inf")
            anteriores[nombre] = None

        distancias[inicio] = 0

        while len(visitados) < len(self.nodos):
            # Buscar el nodo mas cercano que no se ha visitado
            nodo_actual = None
            menor_distancia = float("inf")

            for nombre in self.nodos:
                if nombre not in visitados:
                    if distancias[nombre] < menor_distancia:
                        menor_distancia = distancias[nombre]
                        nodo_actual = nombre

            if nodo_actual is None or nodo_actual == destino:
                break

            visitados.add(nodo_actual)

            # Revisar vecinos
            for vecino, peso in self.nodos[nodo_actual].vecinos.items():
                nueva_distancia = distancias[nodo_actual] + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = nodo_actual

        # Si sigue en infinito es que no se pudo llegar
        if distancias[destino] == float("inf"):
            return None, []

        # Construir el camino de atras hacia adelante
        camino: List[str] = []
        actual: Optional[str] = destino
        while actual is not None:
            camino.append(actual)
            actual = anteriores[actual]

        camino.reverse()
        return distancias[destino], camino
