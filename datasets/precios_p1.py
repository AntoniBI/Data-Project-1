import psycopg2
from psycopg2 import sql
import pandas as pd

# Datos a insertar
data = [
    {"distrito": "Ciutat Vella", "district_id": 1, "precio_max": 2101.5, "precio_min": 1500, "precio_medio": 1900},
    {"distrito": "Pla del Real", "district_id": 2, "precio_max": 2046.8, "precio_min": 1400, "precio_medio": 1800},
    {"distrito": "L'Eixample", "district_id": 3, "precio_max": 2028.0, "precio_min": 1350, "precio_medio": 1850},
    {"distrito": "Quatre Carreres", "district_id": 4, "precio_max": 1800, "precio_min": 1200, "precio_medio": 1500},
    {"distrito": "La Saïdia", "district_id": 5, "precio_max": 1750, "precio_min": 1100, "precio_medio": 1375},
    {"distrito": "Benimaclet", "district_id": 6, "precio_max": 1600, "precio_min": 1000, "precio_medio": 1250},
    {"distrito": "Algirós", "district_id": 7, "precio_max": 1700, "precio_min": 1050, "precio_medio": 1275},
    {"distrito": "Poblats Marítims", "district_id": 8, "precio_max": 1650, "precio_min": 1050, "precio_medio": 1350},
    {"distrito": "Patraix", "district_id": 9, "precio_max": 1500, "precio_min": 1000, "precio_medio": 1250},
    {"distrito": "Campanar", "district_id": 10, "precio_max": 1800, "precio_min": 1200, "precio_medio": 1450},
    {"distrito": "Benicalap", "district_id": 11, "precio_max": 1600, "precio_min": 1100, "precio_medio": 1300},
    {"distrito": "La Xerea", "district_id": 12, "precio_max": 1700, "precio_min": 1200, "precio_medio": 1400},
    {"distrito": "La Roqueta", "district_id": 13, "precio_max": 1600, "precio_min": 1100, "precio_medio": 1325},
    {"distrito": "El Carme", "district_id": 14, "precio_max": 1800, "precio_min": 1200, "precio_medio": 1450},
    {"distrito": "El Pla del Remei", "district_id": 15, "precio_max": 2000, "precio_min": 1300, "precio_medio": 1750},
    {"distrito": "La Creu del Grau", "district_id": 16, "precio_max": 1700, "precio_min": 1100, "precio_medio": 1400},
    {"distrito": "El Cabanyal", "district_id": 17, "precio_max": 1600, "precio_min": 1050, "precio_medio": 1300},
    {"distrito": "Malva-rosa", "district_id": 18, "precio_max": 1500, "precio_min": 1000, "precio_medio": 1225},
    {"distrito": "El Grau", "district_id": 19, "precio_max": 1800, "precio_min": 1200, "precio_medio": 1475},
    {"distrito": "La Malva-rosa", "district_id": 20, "precio_max": 1500, "precio_min": 1000, "precio_medio": 1225}
]

# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(data)

# Conectar a PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="postgres",   # Reemplaza con tu base de datos
        user="postgres",     # Reemplaza con tu usuario
        password="Welcome01",  # Reemplaza con tu contraseña
        host="localhost",    # O la IP de tu servidor de base de datos
        port="5432"          # El puerto de tu servidor de base de datos
    )
    cur = conn.cursor()

    # Crear la tabla en PostgreSQL si no existe
    create_table_query = """
    CREATE TABLE IF NOT EXISTS precios_vivienda (
        distrito VARCHAR(100),
        district_id INT PRIMARY KEY,
        precio_max DECIMAL(10, 2),
        precio_min DECIMAL(10, 2),
        precio_medio DECIMAL(10, 2)
    );
    """
    cur.execute(create_table_query)
    conn.commit()

    # Insertar los datos en la tabla precios_vivienda
    for index, row in df.iterrows():
        insert_query = sql.SQL("""
            INSERT INTO precios_vivienda (distrito, district_id, precio_max, precio_min, precio_medio)
            VALUES (%s, %s, %s, %s, %s)
        """)
        cur.execute(insert_query, (
            row['distrito'], 
            row['district_id'], 
            row['precio_max'], 
            row['precio_min'], 
            row['precio_medio']
        ))

    # Confirmar los cambios (commit)
    conn.commit()

    print("Datos cargados correctamente a PostgreSQL")

except Exception as e:
    print("Error al conectar o insertar datos:", e)

finally:
    # Cerrar el cursor y la conexión
    if cur:
        cur.close()
    if conn:
        conn.close()
