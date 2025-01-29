import psycopg2
import pandas as pd

POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "Welcome01"
}

# Función para conectar a la base de datos
def connect_to_database():
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Función para cargar los datos de precios de vivienda
def load_precios_vivienda():
    conn = connect_to_database()
    if not conn:
        return pd.DataFrame()

    query = "SELECT * FROM precios_vivienda;"
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print("Error cargando los datos de precios de vivienda:", e)
        return pd.DataFrame()
    finally:
        conn.close()

# Función para filtrar los distritos por el rango de precios
def filtrar_distritos_por_precio(df, precio_min, precio_max):
    filtrado = df[(df['precio_medio'] >= precio_min) & (df['precio_medio'] <= precio_max)]
    return filtrado
