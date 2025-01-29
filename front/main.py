import streamlit as st
import pydeck as pdk
import pandas as pd
from precio_vivienda_stream import load_precios_vivienda, filtrar_distritos_por_precio
from hospitales_stream import get_hospitales_data, calcular_puntuacion_hospitales
from distritos_stream import load_distritos
from estaciones_stream import get_estaciones_data, calcular_puntuacion_estaciones
from educativos_stream import get_educativos_data, calcular_puntuacion_educativos


def calcular_color(distrito_id, top_distritos, cumple_precio):
    """
    Asigna el color a los distritos según los criterios:
    - Verde más oscuro para el mejor distrito.
    - Verde medio para el segundo mejor distrito.
    - Verde más claro para el tercer mejor distrito.
    - Verde genérico para distritos que cumplen el filtro de precio pero no están en el top 3.
    - Gris para distritos que no cumplen el filtro de precio.
    """
    if distrito_id in top_distritos:
        rank = top_distritos.index(distrito_id)
        colores_top = [
            [0, 128, 0, 150],  # Verde oscuro
            [0, 200, 0, 150],  # Verde medio
            [0, 255, 0, 150],  # Verde claro
        ]
        return colores_top[rank]
    elif cumple_precio:
        return [144, 238, 144, 150]  # Verde genérico para distritos que cumplen el precio
    else:
        return [169, 169, 169, 100]  # Gris para los que no cumplen el precio


def main():
    st.title("Mapa por Distritos en Valencia")
    st.write("Aplicación para visualizar distritos en función de precios, hospitales, estaciones y centros educativos.")

    # Cargar datos de distritos
    distritos_data = load_distritos()

    # Filtro de precios
    st.sidebar.header("Filtro de Precios")
    precio_min = st.sidebar.slider("Precio mínimo", min_value=500, max_value=4500, value=800, step=50)
    precio_max = st.sidebar.slider("Precio máximo", min_value=500, max_value=4500, value=1200, step=50)

    # Validación del rango de precios
    if precio_min > precio_max:
        st.sidebar.error("El precio mínimo no puede ser mayor que el precio máximo. Ajusta los valores.")
        st.stop()

    precios_data = load_precios_vivienda()
    precios_filtrados = filtrar_distritos_por_precio(precios_data, precio_min, precio_max)

    # Filtro de hospitales
    st.sidebar.header("Filtro de Hospitales")
    importancia_hospitales = st.sidebar.selectbox(
        "Importancia de hospitales",
        ["Muy poca importancia", "Poca importancia", "Importancia media", "Importancia alta"]
    )
    hospitales_data = get_hospitales_data()
    hospitales_data = calcular_puntuacion_hospitales(hospitales_data, importancia_hospitales)

    # Filtro de estaciones
    st.sidebar.header("Filtro de Estaciones")
    importancia_estaciones = st.sidebar.selectbox(
        "Importancia de estaciones",
        ["Muy poca importancia", "Poca importancia", "Importancia media", "Importancia alta"]
    )
    estaciones_data = get_estaciones_data()
    estaciones_data = calcular_puntuacion_estaciones(estaciones_data, importancia_estaciones)

    # Filtro de educativos
    st.sidebar.header("Filtro de Centros Educativos")
    importancia_educativos = st.sidebar.selectbox(
        "Importancia de centros educativos",
        ["Muy poca importancia", "Poca importancia", "Importancia media", "Importancia alta"]
    )
    educativos_data = get_educativos_data()
    educativos_data = calcular_puntuacion_educativos(educativos_data, importancia_educativos)

    # Combinar datos
    distritos_data = distritos_data.merge(precios_filtrados, on="district_id", how="left")
    distritos_data = distritos_data.merge(hospitales_data, on="district_id", how="left")
    distritos_data = distritos_data.merge(estaciones_data, on="district_id", how="left")
    distritos_data = distritos_data.merge(educativos_data, on="district_id", how="left")

    # Reemplazar valores NaN en las columnas de puntuaciones con 0
    distritos_data["puntuacion_hospitales"].fillna(0, inplace=True)
    distritos_data["puntuacion_estaciones"].fillna(0, inplace=True)
    distritos_data["puntuacion_educativos"].fillna(0, inplace=True)

    # Calcular puntuación total (hospitales + estaciones + educativos)
    distritos_data["puntuacion_total"] = (
        distritos_data["puntuacion_hospitales"] +
        distritos_data["puntuacion_estaciones"] +
        distritos_data["puntuacion_educativos"]
    )

    # Filtrar distritos que cumplen con el rango de precios
    distritos_filtrados = distritos_data[
        (distritos_data["precio_medio"] >= precio_min) &
        (distritos_data["precio_medio"] <= precio_max)
    ]

    # Seleccionar los 3 distritos con mayor puntuación total
    top_distritos = distritos_filtrados.nlargest(3, "puntuacion_total")["district_id"].tolist()

    # Configurar el color del mapa
    distritos_data["color"] = distritos_data.apply(
        lambda row: calcular_color(
            row["district_id"],
            top_distritos,
            row["precio_medio"] >= precio_min and row["precio_medio"] <= precio_max
        ),
        axis=1
    )

    # Crear capa GeoJson
    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        data=distritos_data,
        get_fill_color="color",
        get_line_color=[0, 0, 0, 200],
        line_width_min_pixels=1,
        pickable=True,
    )

    # Configuración del mapa
    view_state = pdk.ViewState(
        latitude=39.4699,
        longitude=-0.3763,
        zoom=12,
        pitch=0
    )

    # Estilo de Mapbox
    mapbox_style = "mapbox://styles/mapbox/streets-v11"

    # Tooltip del mapa
    tooltip = {
        "html": """
        <b>Distrito:</b> {nombre_distrito}<br>
        <b>Precio medio:</b> {precio_medio}<br>
        <b>Hospitales:</b> {total_hospitales}<br>
        <b>Estaciones:</b> {total_stops}<br>
        <b>Educativos:</b> {total_centros_educativos}<br>
        <b>Puntuación Total:</b> {puntuacion_total}
        """,
        "style": {"backgroundColor": "white", "color": "black"}
    }

    # Mostrar mapa
    r = pdk.Deck(
        layers=[geojson_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style=mapbox_style  
    )
    st.pydeck_chart(r)

    st.subheader("Precio medio de viviendas por distrito dentro del rango seleccionado")
    if not distritos_filtrados.empty:
        tabla_data = distritos_filtrados[["nombre_distrito", "precio_medio"]].drop_duplicates().sort_values(by="precio_medio", ascending=False)
        st.table(tabla_data)
    else:
        st.write("No hay distritos que cumplan con el rango de precios seleccionado.")

    st.subheader("Nuestras recomendaciones")
    if top_distritos:
        nombres_top = distritos_filtrados[distritos_filtrados["district_id"].isin(top_distritos)]["nombre_distrito"].unique()
        st.write("Basándonos en tus preferencias, te recomendamos vivir en los siguientes distritos:")
        for nombre in nombres_top:
            st.write(f"- {nombre}")
    else:
        st.write("No se encontraron distritos recomendados según tus preferencias.")

if __name__ == "__main__":
    main()










