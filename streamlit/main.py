import streamlit as st
import pydeck as pdk
from precio_vivienda import load_precios_vivienda, filtrar_distritos_por_precio
from hospitales_stream import get_hospitales_data, calcular_puntuacion_hospitales
from distritos_stream import load_distritos
from estaciones_stream import get_estaciones_data, calcular_puntuacion_estaciones
from educativos_stream import get_educativos_data, calcular_puntuacion_educativos

def calcular_color(precio_filtrado, puntuacion_total):
    """Calcular el color de un distrito basado en los filtros."""
    if not precio_filtrado:
        return [169, 169, 169, 100]  # Gris si el precio no está en el rango
    else:
        intensidad = int(puntuacion_total * 255)
        return [0, intensidad, 0, 150]  # Escala de verde

def main():
    st.title("Mapa por Distritos en Valencia")
    st.write("Aplicación para visualizar distritos en función de precios, hospitales y estaciones.")

    # Cargar datos de distritos
    distritos_data = load_distritos()

    # Filtro de precios
    st.sidebar.header("Filtro de Precios")
    precio_min = st.sidebar.slider("Precio mínimo", min_value=500, max_value=2000, value=800, step=50)
    precio_max = st.sidebar.slider("Precio máximo", min_value=500, max_value=2000, value=1200, step=50)
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

    # Combinar datos
    distritos_data = distritos_data.merge(precios_filtrados, on="district_id", how="left")
    distritos_data = distritos_data.merge(hospitales_data, on="district_id", how="left")
    distritos_data = distritos_data.merge(estaciones_data, on="district_id", how="left")

    # Calcular puntuación total (hospitales + estaciones)
    distritos_data["puntuacion_total"] = (
        distritos_data["puntuacion_hospitales"] + distritos_data["puntuacion_estaciones"]
    )

    # Configurar el color del mapa
    distritos_data["color"] = distritos_data.apply(
        lambda row: calcular_color(row["precio_medio"] >= precio_min and row["precio_medio"] <= precio_max,
                                   row["puntuacion_total"]), axis=1
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

    # Aquí se establece el estilo de Mapbox
    mapbox_style = "mapbox://styles/mapbox/streets-v11"

    tooltip = {
        "html": """
        <b>Distrito:</b> {nombre_distrito}<br>
        <b>Precio medio:</b> {precio_medio}<br>
        <b>Hospitales:</b> {total_hospitales}<br>
        <b>Estaciones:</b> {total_stops}<br>
        """,
        "style": {"backgroundColor": "white", "color": "black"}
    }

    # Mostrar mapa con el estilo de Mapbox
    r = pdk.Deck(
        layers=[geojson_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style=mapbox_style  # Aquí se aplica el estilo
    )
    st.pydeck_chart(r)


if __name__ == "__main__":
    main()



# import streamlit as st
# import pydeck as pdk
# from precio_vivienda import load_precios_vivienda, filtrar_distritos_por_precio
# from hospitales_stream import get_hospitales_data, calcular_puntuacion_hospitales
# from distritos_stream import load_distritos
# from estaciones_stream import get_estaciones_data, calcular_puntuacion_estaciones
# from educativos_stream import get_educativos_data, calcular_puntuacion_educativos

# def calcular_color(precio_filtrado, puntuacion_total):
#     """Calcular el color de un distrito basado en los filtros."""
#     if not precio_filtrado:
#         return [169, 169, 169, 100]  # Gris si el precio no está en el rango
#     else:
#         intensidad = int(puntuacion_total * 255)
#         return [0, intensidad, 0, 150]  # Escala de verde

# def main():
#     st.title("Mapa por Distritos en Valencia")
#     st.write("Aplicación para visualizar distritos en función de precios, hospitales y estaciones.")

#     # Cargar datos de distritos
#     distritos_data = load_distritos()

#     # Filtro de precios
#     st.sidebar.header("Filtro de Precios")
#     precio_min = st.sidebar.slider("Precio mínimo", min_value=500, max_value=2000, value=800, step=50)
#     precio_max = st.sidebar.slider("Precio máximo", min_value=500, max_value=2000, value=1200, step=50)
#     precios_data = load_precios_vivienda()
#     precios_filtrados = filtrar_distritos_por_precio(precios_data, precio_min, precio_max)

#     # Filtro de hospitales
#     st.sidebar.header("Filtro de Hospitales")
#     importancia_hospitales = st.sidebar.selectbox(
#         "Importancia de hospitales",
#         ["Muy poca importancia", "Poca importancia", "Importancia media", "Importancia alta"]
#     )
#     hospitales_data = get_hospitales_data()
#     hospitales_data = calcular_puntuacion_hospitales(hospitales_data, importancia_hospitales)

#     # Filtro de estaciones
#     st.sidebar.header("Filtro de Estaciones")
#     importancia_estaciones = st.sidebar.selectbox(
#         "Importancia de estaciones",
#         ["Muy poca importancia", "Poca importancia", "Importancia media", "Importancia alta"]
#     )
#     estaciones_data = get_estaciones_data()
#     estaciones_data = calcular_puntuacion_estaciones(estaciones_data, importancia_estaciones)


#   # Filtro de educativos
#     st.sidebar.header("Filtro de Centros Educativos")
#     importancia_educativos = st.sidebar.selectbox(
#         "Importancia de centros educativos",
#         ["Muy poca importancia", "Poca importancia", "Importancia media", "Importancia alta"]
#     )
#     educativos_data = get_educativos_data()
#     educativos_data = calcular_puntuacion_educativos(educativos_data, importancia_educativos)

#     # Combinar datos
#     distritos_data = distritos_data.merge(precios_filtrados, on="district_id", how="left")
#     distritos_data = distritos_data.merge(hospitales_data, on="district_id", how="left")
#     distritos_data = distritos_data.merge(estaciones_data, on="district_id", how="left")
#     distritos_data = distritos_data.merge(educativos_data, on="district_id", how="left")

#     # Calcular puntuación total (hospitales + estaciones + educativos)
#     distritos_data["puntuacion_total"] = (
#         distritos_data["puntuacion_hospitales"] + distritos_data["puntuacion_estaciones"]+ distritos_data["puntuacion_educativos"]
#     )

#     # Configurar el color del mapa
#     distritos_data["color"] = distritos_data.apply(
#         lambda row: calcular_color(row["precio_medio"] >= precio_min and row["precio_medio"] <= precio_max,
#                                    row["puntuacion_total"]), axis=1
#     )

#     # Crear capa GeoJson
#     geojson_layer = pdk.Layer(
#         "GeoJsonLayer",
#         data=distritos_data,
#         get_fill_color="color",
#         get_line_color=[0, 0, 0, 200],
#         line_width_min_pixels=1,
#         pickable=True,
#     )

#     # Configuración del mapa
#     view_state = pdk.ViewState(
#         latitude=39.4699,
#         longitude=-0.3763,
#         zoom=12,
#         pitch=0
#     )

#     # Aquí se establece el estilo de Mapbox
#     mapbox_style = "mapbox://styles/mapbox/streets-v11"

#     tooltip = {
#         "html": """
#         <b>Distrito:</b> {nombre_distrito}<br>
#         <b>Precio medio:</b> {precio_medio}<br>
#         <b>Hospitales:</b> {total_hospitales}<br>
#         <b>Estaciones:</b> {total_stops}<br>
#         <b>Educativos:</b> {total_centros_educativos}
#         """,
#         "style": {"backgroundColor": "white", "color": "black"}
#     }

#     # Mostrar mapa con el estilo de Mapbox
#     r = pdk.Deck(
#         layers=[geojson_layer],
#         initial_view_state=view_state,
#         tooltip=tooltip,
#         map_style=mapbox_style  # Aquí se aplica el estilo
#     )
#     st.pydeck_chart(r)


# if __name__ == "__main__":
#     main()

