import psycopg2
import pandas as pd

# Conexión a PostgreSQL
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",   # Reemplaza con tu base de datos
            user="postgres",     # Reemplaza con tu usuario
            password="Welcome01", # Reemplaza con tu contraseña
            host="localhost",    # O la IP de tu servidor de base de datos
            port="5432"          # El puerto de tu servidor de base de datos
        )
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Obtener datos de hospitales
def get_estaciones_data():
    conn = connect_to_db()
    if not conn:
        return None
    try:
        query = "SELECT district_id, total_stops, normalized_total_stops FROM total_estaciones ;"
        df = pd.read_sql_query(query, conn)  # Leer datos en un DataFrame
        conn.close()
        print("Estaciones DataFrame:", df.head())  # Verifica las columnas y datos
        return df
    except Exception as e:
        print("Error al obtener datos de estaciones:", e)
        if conn:
            conn.close()
        return None

# Calcular puntuación de estaciones en función de la importancia
def calcular_puntuacion_estaciones(df, importancia):
    ponderacion = {
        "Muy poca importancia": 0.25,
        "Poca importancia": 0.5,
        "Importancia media": 0.75,
        "Importancia alta": 1.0
    }
    peso = ponderacion.get(importancia, 0.5)  # Por defecto, importancia media

    # Verificar si la columna existe antes de calcular la puntuación
    if "normalized_total_stops" not in df.columns:
        raise KeyError("La columna 'total_estaciones_normalizado' no existe en el DataFrame.")
    
    df["puntuacion_estaciones"] = df["normalized_total_stops"] * peso
    return df

