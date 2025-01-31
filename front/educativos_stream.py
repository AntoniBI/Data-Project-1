import psycopg2
import pandas as pd

import sys
import pg8000.native
conn = pg8000.native.Connection("postgres", password="Welcome01", host="postgres")

# Conexión a PostgreSQL
def connect_to_db():
    try:
        conn = psycopg2.connect(
            user="postgres",     
            password="Welcome01", 
            host="postgres",    
            port="5432"          
        )
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Obtener datos de centros educativos
def get_educativos_data():
    conn = connect_to_db()
    if not conn:
        return None
    try:
        query = "SELECT district_id, total_centros_educativos, normalized_total_centros_educativos FROM centros_educativos ;"
        df = pd.read_sql_query(query, conn)  # Leer datos en un DataFrame
        conn.close()
        print("Centros_Educativos DataFrame:", df.head())  # Verifica las columnas y datos
        return df
    except Exception as e:
        print("Error al obtener datos de educativos:", e)
        if conn:
            conn.close()
        return None

# Calcular puntuación de estaciones en función de la importancia
def calcular_puntuacion_educativos(df, importancia):
    ponderacion = {
        "Muy poca importancia": 0.25,
        "Poca importancia": 0.5,
        "Importancia media": 0.75,
        "Importancia alta": 1.0
    }
    peso = ponderacion.get(importancia, 0.5)  # Por defecto, importancia media

    # Verificar si la columna existe antes de calcular la puntuación
    if "normalized_total_centros_educativos" not in df.columns:
        raise KeyError("La columna 'normalized_total_centros_educativos' no existe en el DataFrame.")
    
    df["puntuacion_educativos"] = df["normalized_total_centros_educativos"] * peso
    return df

