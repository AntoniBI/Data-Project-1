import streamlit as st
import pandas as pd
from distritos_stream import load_distritos, dibujar_distritos
from precio_vivienda import load_precios_vivienda, filtrar_distritos_por_precio

# Título de la aplicación
st.title("Mapa de Distritos en Valencia con Filtros de Precio")
st.write("Este mapa muestra los distritos de Valencia con la opción de filtrar por rango de precios.")

# Cargar los datos de distritos y precios
distritos_data = load_distritos()
precios_data = load_precios_vivienda()

if distritos_data.empty or precios_data.empty:
    st.warning("No se pudieron cargar los datos.")
else:
    # Filtros de precio
    precio_min = st.number_input("Precio mínimo", min_value=0, value=1000)
    precio_max = st.number_input("Precio máximo", min_value=0, value=5000)

    # Filtrar los distritos por precio
    precios_filtrados = filtrar_distritos_por_precio(precios_data, precio_min, precio_max)

    # Filtrar los distritos por aquellos que están dentro del rango de precios
    distritos_filtrados = distritos_data[distritos_data["district_id"].isin(precios_filtrados["district_id"])]

    # Dibujar los distritos en el mapa con el filtro aplicado
    dibujar_distritos(distritos_data, distritos_filtrados)
