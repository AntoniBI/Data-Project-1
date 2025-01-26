import streamlit as st
import pandas as pd
import pydeck as pdk
import psycopg2
import json  # Necesario para convertir las geometrías a objetos Python

# Configuración de la conexión a PostgreSQL
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
        district_id AS id_distrito,
        nombre_distrito,
        ST_AsGeoJSON(geo_shape) AS geometry  -- Convertir la geometría a GeoJSON
    FROM public.distritos;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            # Convertir los datos en un DataFrame
            df = pd.DataFrame(rows, columns=["id_distrito", "nombre_distrito", "geometry"])
            # Convertir la columna de geometría (GeoJSON) a objetos Python
            df["geometry"] = df["geometry"].apply(json.loads)
            return df
    except Exception as e:
        st.error(f"Error cargando los datos: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Función para cargar los datos de estaciones y contar cuántas hay por distrito
def load_estaciones_por_distrito():
    conn = connect_to_database()
    if not conn:
        return pd.DataFrame()

    query = """
    SELECT 
        district_id, 
        COUNT(*) AS total_estaciones
    FROM public.estaciones
    GROUP BY district_id;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            # Convertir los datos en un DataFrame
            df = pd.DataFrame(rows, columns=["id_distrito", "total_estaciones"])
            return df
    except Exception as e:
        st.error(f"Error cargando los datos de estaciones: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Función para cargar los datos de hospitales y contar cuántos hay por distrito
def load_hospitales_por_distrito():
    conn = connect_to_database()
    if not conn:
        return pd.DataFrame()

    query = """
    SELECT 
        district_id, 
        COUNT(*) AS total_hospitales
    FROM public.hospitales
    GROUP BY district_id;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            # Convertir los datos en un DataFrame
            df = pd.DataFrame(rows, columns=["id_distrito", "total_hospitales"])
            return df
    except Exception as e:
        st.error(f"Error cargando los datos de hospitales: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Aplicación principal de Streamlit
def main():
    st.title("Mapa de Distritos, Estaciones y Hospitales en Valencia")
    st.write("Este mapa muestra las áreas de los distritos en Valencia junto con el número de estaciones y hospitales en cada uno.")

    # Cargar los datos de distritos, estaciones y hospitales
    data_distritos = load_distritos()
    data_estaciones = load_estaciones_por_distrito()
    data_hospitales = load_hospitales_por_distrito()

    if data_distritos.empty or data_estaciones.empty or data_hospitales.empty:
        st.warning("No se pudieron cargar los datos.")
        return

    # Unir los datos de distritos con estaciones y hospitales (por el id_distrito)
    data = pd.merge(data_distritos, data_estaciones, on="id_distrito", how="left")
    data = pd.merge(data, data_hospitales, on="id_distrito", how="left")

    # Crear una capa de polígonos con la geometría de los distritos
    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        data=data,
        get_fill_color=[200, 0, 0, 100],  # Color rojo con opacidad
        get_line_color=[0, 0, 0, 200],  # Bordes negros más opacos
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
        <b>ID:</b> {id_distrito}<br>
        <b>Total de Estaciones:</b> {total_estaciones}<br>
        <b>Total de Hospitales:</b> {total_hospitales}
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

if __name__ == "__main__":
    main()
