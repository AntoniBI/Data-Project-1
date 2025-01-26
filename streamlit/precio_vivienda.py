# import psycopg2
# import pandas as pd

# # Conexión a PostgreSQL
# def connect_to_db():
#     try:
#         conn = psycopg2.connect(
#             dbname="postgres",   # Reemplaza con tu base de datos
#             user="postgres", # Reemplaza con tu usuario
#             password="Welcome01",  # Reemplaza con tu contraseña
#             host="localhost",  # O la IP de tu servidor de base de datos
#             port="5432"        # El puerto de tu servidor de base de datos
#         )
#         return conn
#     except Exception as e:
#         print("Error al conectar a la base de datos:", e)
#         return None

# # Obtener datos de la tabla precios_vivienda
# def get_precios_data():
#     conn = connect_to_db()
#     if not conn:
#         return None
#     try:
#         query = "SELECT * FROM precios_vivienda;"
#         df = pd.read_sql_query(query, conn)  # Leer datos en un DataFrame
#         conn.close()
#         return df
#     except Exception as e:
#         print("Error al obtener datos de la base de datos:", e)
#         if conn:
#             conn.close()
#         return None

# # Filtrar distritos por rango de precios
# def filtrar_distritos_por_precio(df, precio_min, precio_max):
#     filtrado = df[(df['precio_medio'] >= precio_min) & (df['precio_medio'] <= precio_max)]
#     return filtrado

import psycopg2
import pandas as pd

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
