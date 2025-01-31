from pymongo import MongoClient
import pandas as pd
import psycopg2
from psycopg2 import sql

MONGO_URI = "mongodb://root:example@mongo:27017"
DB_NAME = "dataproject1"
COLLECTION_NAME = "preciosviv"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

pipeline = [
    {
        "$match": { "precio_2022_euros_m2": { "$exists": True, "$ne": None } }
    },
    {
        "$group": {
            "_id": {
                "coddistrit": "$coddistrit",
                "distrito": "$distrito"
            },
            "precio_max": {"$max": "$precio_2022_euros_m2"},
            "precio_min": {"$min": "$precio_2022_euros_m2"},
            "precio_medio": {"$avg": "$precio_2022_euros_m2"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "district_id": "$_id.coddistrit",
            "distrito": "$_id.distrito",
            "precio_max": 1,
            "precio_min": 1,
            "precio_medio": {"$round": ["$precio_medio", 2]}
        }
    }
]

data = list(collection.aggregate(pipeline))

# Añadir manualmente datos estimados para distritos sin información
manual_entries = [
    {"district_id": 17, "distrito": "Pobles del Nord", "precio_max": 1300, "precio_min": 1000, "precio_medio": 1150},
    {"district_id": 18, "distrito": "Pobles de l'Oest", "precio_max": 1600, "precio_min": 1200, "precio_medio": 1400},
    {"district_id": 19, "distrito": "Pobles del Sud", "precio_max": 1450, "precio_min": 1100, "precio_medio": 1275},
]

# Extender la lista con los datos manuales
data.extend(manual_entries)
df = pd.DataFrame(data)

try:
    con = psycopg2.connect(
        user="postgres",
        password="Welcome01",
        host="postgres",
        port="5432",
    )
    cur = con.cursor()

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
    con.commit()

    insert_query = sql.SQL("""
        INSERT INTO precios_vivienda (distrito, district_id, precio_max, precio_min, precio_medio)
        VALUES (%s, %s, %s, %s, %s)
    """)

    for _, row in df.iterrows():
        cur.execute(insert_query, (
            row['distrito'], 
            row['district_id'], 
            row['precio_max'], 
            row['precio_min'], 
            row['precio_medio']
        ))

    con.commit()

finally:
    # Cerrar conexiones
    if 'cur' in locals():
        cur.close()
    if 'con' in locals():
        con.close()