import streamlit as st
import psycopg2
import pandas as pd

# Configuración de la conexión a PostgreSQL
POSTGRES_CONFIG = {
    "host": "localhost",  # Cambia según tu configuración
    "port": 5432,
    "database": "postgres",  # Nombre de tu base de datos
    "user": "postgres",
    "password": "Welcome01"  # Cambia tu contraseña
}

# Función para conectar a la base de datos
def connect_to_database():
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Error conectando a la base de datos: {e}")
        return None

# Función para cargar el total de estaciones por distrito
def cargar_datos():
    conn = connect_to_database()
    if not conn:
        return pd.DataFrame()  # Retorna un DataFrame vacío si no hay conexión

    query = """
    SELECT 
        district_id AS distrito,
        total_stops AS total_estaciones
    FROM 
        total_estaciones;
    """
    try:
        data = pd.read_sql_query(query, conn)
        return data
    except Exception as e:
        st.error(f"Error cargando los datos: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Función principal de la aplicación Streamlit
def main():
    st.title("Total de Estaciones por Distrito")
    st.write("Esta tabla muestra el número total de estaciones por distrito.")

    # Cargar los datos
    data = cargar_datos()

    if data.empty:
        st.warning("No se encontraron datos.")
        return

    # Mostrar los datos en una tabla interactiva
    st.dataframe(data)

    # Opcional: Mostrar un gráfico de barras
    st.bar_chart(data.set_index("distrito"))

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
