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

# Obtener datos de hospitales
def get_hospitales_data():
    conn = connect_to_db()
    if not conn:
        return None
    try:
        query = "SELECT district_id, total_hospitales, total_hospitales_normalizado FROM hospitales_totales_distrito;"
        df = pd.read_sql_query(query, conn)  # Leer datos en un DataFrame
        conn.close()
        print("Hospitales DataFrame:", df.head())  # Verifica las columnas y datos
        return df
    except Exception as e:
        print("Error al obtener datos de hospitales:", e)
        if conn:
            conn.close()
        return None

# Calcular puntuación de hospitales en función de la importancia
def calcular_puntuacion_hospitales(df, importancia):
    ponderacion = {
        "Muy poca importancia": 0.25,
        "Poca importancia": 0.5,
        "Importancia media": 0.75,
        "Importancia alta": 1.0
    }
    peso = ponderacion.get(importancia, 0.5)  # Por defecto, importancia media

    # Verificar si la columna existe antes de calcular la puntuación
    if "total_hospitales_normalizado" not in df.columns:
        raise KeyError("La columna 'total_hospitales_normalizado' no existe en el DataFrame.")
    
    df["puntuacion_hospitales"] = df["total_hospitales_normalizado"] * peso
    return df

