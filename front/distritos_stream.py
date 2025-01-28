import streamlit as st
import pandas as pd
import pydeck as pdk
import psycopg2
import json

POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "Welcome01"
}

# Función para conectar a la base de datos
def connect_to_database():
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Error conectando a la base de datos: {e}")
        return None

# Función para cargar los datos de los distritos
def load_distritos():
    conn = connect_to_database()
    if not conn:
        return pd.DataFrame()

    query = """
    SELECT 
        district_id,
        nombre_distrito,
        ST_AsGeoJSON(geo_shape) AS geometry
    FROM public.distritos;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows, columns=["district_id", "nombre_distrito", "geometry"])
            df["geometry"] = df["geometry"].apply(json.loads)
            return df
    except Exception as e:
        st.error(f"Error cargando los datos de los distritos: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Función para dibujar los distritos en el mapa
def dibujar_distritos(distritos_data, distritos_filtrados):
    # Agregar una columna para el color de cada distrito
    distritos_data['color'] = distritos_data['district_id'].apply(
        lambda x: [0, 255, 0, 100] if x in distritos_filtrados["district_id"].values else [169, 169, 169, 100]
    )

    # Crear una capa de polígonos con la geometría de los distritos
    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        data=distritos_data,
        get_fill_color="color",  # Utiliza la columna "color" para definir el color de relleno
        get_line_color=[0, 0, 0, 200],  # Bordes negros
        line_width_min_pixels=1,
        pickable=True,
    )

    # Configuración inicial del mapa
    view_state = pdk.ViewState(
        latitude=39.4699,  # Coordenadas aproximadas de Valencia
        longitude=-0.3763,
        zoom=12,
        pitch=0
    )

    # Crear un tooltip para mostrar información del distrito
    tooltip = {
        "html": """
        <b>Distrito:</b> {nombre_distrito}<br>
        <b>ID:</b> {district_id}
        """,
        "style": {"backgroundColor": "white", "color": "black"}
    }

    # Configurar el mapa
    r = pdk.Deck(
        layers=[geojson_layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/streets-v11",
        tooltip=tooltip
    )

    # Mostrar el mapa en Streamlit
    st.pydeck_chart(r)
