

import csv
import os
from typing import List

import pandas as pd
import streamlit as st

from grafo import Grafo
from io_handler import cargar_grafo

st.set_page_config(
    page_title="Mi proyecto 3",
    page_icon="🚇",
    layout="wide",
)

RUTA_CSV = "nodos.csv"
COLUMNAS = ["Origen", "Destino", "Peso"]

# El grafo se carga una sola vez y se guarda entre recargas
if "grafo" not in st.session_state:
    st.session_state.grafo = cargar_grafo()

# Mensaje que debe sobrevivir al st.rerun()
if "mensaje" not in st.session_state:
    st.session_state.mensaje = ""


def obtener_grafo() -> Grafo:
    """Regresa el grafo guardado en session_state."""
    return st.session_state.grafo


def leer_dataframe(ruta: str) -> pd.DataFrame:
    """Lee el CSV con pandas. Si no existe o esta vacio regresa uno vacio."""
    try:
        return pd.read_csv(ruta)
    except FileNotFoundError:
        st.warning("Todavia no existe el archivo " + ruta)
    except pd.errors.EmptyDataError:
        st.warning("El archivo " + ruta + " esta vacio")
    return pd.DataFrame(columns=COLUMNAS)


def registrar_conexion(origen: str, destino: str, peso: float) -> None:
    """Guarda la conexion en el CSV y la agrega al grafo en memoria."""
    existe = os.path.exists(RUTA_CSV)

    with open(RUTA_CSV, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        if not existe:
            escritor.writeheader()
        escritor.writerow(
            {"Origen": origen, "Destino": destino, "Peso": peso}
        )

    obtener_grafo().agregar_arista(origen, destino, peso)


def mostrar_sidebar() -> None:
    """Barra lateral con resumen de la red y descarga del CSV."""
    grafo = obtener_grafo()
    df = leer_dataframe(RUTA_CSV)

    st.sidebar.title("🚇 Red de transporte")
    st.sidebar.caption("Proyecto 3 - Miguel Angel Torres Monroy")
    st.sidebar.divider()

    st.sidebar.metric("Estaciones", len(grafo.nodos))
    st.sidebar.metric("Conexiones", len(df))

    st.sidebar.divider()
    with st.sidebar.expander("Estaciones registradas"):
        st.write(", ".join(sorted(grafo.nodos)) or "Ninguna")

    try:
        with open(RUTA_CSV, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        st.sidebar.download_button(
            label="📥 Descargar nodos.csv",
            data=contenido,
            file_name="nodos.csv",
            mime="text/csv",
        )
    except FileNotFoundError:
        st.sidebar.info("Aun no hay archivo para descargar.")


def seccion_agregar() -> None:
    """1. Formulario para agregar nodos al CSV y al grafo."""
    st.subheader("Agregar nodos")

    # Mostrar el mensaje guardado antes del rerun
    if st.session_state.mensaje:
        st.success(st.session_state.mensaje)
        st.session_state.mensaje = ""

    col1, col2, col3 = st.columns(3)
    with col1:
        nodo_origen = st.text_input("Agrega el Origen").strip().upper()
    with col2:
        nodo_destino = st.text_input("Agrega el destino").strip().upper()
    with col3:
        peso_tramo = st.number_input(
            "Peso / Distancia", min_value=0.0, step=1.0
        )

    if st.button("Registrar conexión", type="primary"):
        if nodo_origen == "" or nodo_destino == "":
            st.error("El origen y el destino no pueden ir vacios.")
        elif nodo_origen == nodo_destino:
            st.error("El origen y el destino no pueden ser iguales.")
        elif peso_tramo <= 0:
            st.error("El peso debe ser mayor a 0.")
        else:
            try:
                registrar_conexion(nodo_origen, nodo_destino, peso_tramo)
                st.session_state.mensaje = (
                    f"Conexión registrada: {nodo_origen} - "
                    f"{nodo_destino} = {peso_tramo}"
                )
                st.rerun()
            except OSError as error:
                st.error(f"No se pudo guardar en el archivo: {error}")


def seccion_dijkstra() -> None:
    """2. Elegir origen y destino y ejecutar Dijkstra."""
    st.subheader("Ejecución Dijkstra")
    grafo = obtener_grafo()
    nodos: List[str] = sorted(grafo.nodos)

    if len(nodos) < 2:
        st.info("Se necesitan al menos 2 estaciones para buscar una ruta.")
        return

    col1, col2 = st.columns(2)
    with col1:
        select_origen = st.selectbox("Seleccione el origen", nodos)
    with col2:
        select_destino = st.selectbox(
            "Seleccione el destino", nodos, index=len(nodos) - 1
        )

    costo, camino = grafo.dijkstra(select_origen, select_destino)

    if camino:
        st.success(f"Camino recorrido: {' → '.join(camino)}")

        col_a, col_b = st.columns(2)
        col_a.metric("Costo total", costo)
        col_b.metric("Estaciones recorridas", len(camino))

        # Tabla y grafica de cada tramo
        tramos = []
        for i in range(len(camino) - 1):
            a = camino[i]
            b = camino[i + 1]
            tramos.append(
                {"Tramo": f"{a} → {b}", "Peso": grafo.nodos[a].vecinos[b]}
            )

        if tramos:
            with st.expander("Ver recorrido paso a paso"):
                df_tramos = pd.DataFrame(tramos)
                st.dataframe(df_tramos, hide_index=True)
                st.bar_chart(df_tramos, x="Tramo", y="Peso")
    else:
        st.error(
            f"No existe ruta entre {select_origen} y {select_destino}"
        )


def seccion_datos() -> None:
    """3. Mostrar el CSV como DataFrame."""
    st.subheader("Visualización de datos")
    df = leer_dataframe(RUTA_CSV)

    if df.empty:
        st.info("No hay conexiones registradas.")
        return

    st.dataframe(df, use_container_width=True, hide_index=True)

    try:
        # Si alguien escribio texto en el peso, se vuelve NaN y no cuenta
        df["Peso"] = pd.to_numeric(df["Peso"], errors="coerce")
        st.write("Peso total por estación de origen:")
        st.bar_chart(df.groupby("Origen")["Peso"].sum())
    except KeyError as error:
        st.error(f"Falta la columna {error} en el CSV.")


# ---------------- Pagina ----------------
st.title("Mi proyecto 3")
st.caption("Algoritmo de Dijkstra")

mostrar_sidebar()

tab1, tab2, tab3 = st.tabs(
    ["Agregar nodos", "Dijkstra", "Datos"]
)

with tab1:
    seccion_agregar()

with tab2:
    seccion_dijkstra()

with tab3:
    seccion_datos()
