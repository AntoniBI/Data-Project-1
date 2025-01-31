import pymongo
import psycopg2
import pandas as pd

myclient = pymongo.MongoClient("mongodb://root:example@mongo:27017")
mydb = myclient["dataproject1"]
mycol = mydb["hospitales"]

data = list(mycol.find({}, {"_id": 0, "nombre": 1, "coddistrit": 1, "tipo": 1}))  # Seleccionar solo los campos necesarios
df = pd.DataFrame(data)

df["coddistrit"] = df["coddistrit"].astype(int)  # Convertir el código de distrito a entero

# Agrupar por distrito y contar hospitales
totales_por_distrito = df.groupby("coddistrit").size().reset_index(name="total_hospitales")

max_hospitales = totales_por_distrito["total_hospitales"].max()
totales_por_distrito["total_hospitales_normalizado"] = totales_por_distrito["total_hospitales"] / max_hospitales

# Convertir los datos del DataFrame a tipos nativos de Python
totales_por_distrito["coddistrit"] = totales_por_distrito["coddistrit"].astype(int)
totales_por_distrito["total_hospitales"] = totales_por_distrito["total_hospitales"].astype(int)
totales_por_distrito["total_hospitales_normalizado"] = totales_por_distrito["total_hospitales_normalizado"].astype(float)

con = psycopg2.connect(
    user="postgres",
    password="Welcome01",
    host="postgres",
    port=5432
)
cursor = con.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS public."hospitales_totales_distrito" (
        district_id INTEGER PRIMARY KEY,
        total_hospitales INTEGER NOT NULL,
        total_hospitales_normalizado FLOAT NOT NULL
    );
""")

for _, row in totales_por_distrito.iterrows():
    cursor.execute("""
        INSERT INTO public."hospitales_totales_distrito" (district_id, total_hospitales, total_hospitales_normalizado)
        VALUES (%s, %s, %s)
        ON CONFLICT (district_id) DO UPDATE
        SET total_hospitales = EXCLUDED.total_hospitales,
            total_hospitales_normalizado = EXCLUDED.total_hospitales_normalizado;
    """, (int(row["coddistrit"]), int(row["total_hospitales"]), float(row["total_hospitales_normalizado"])))


con.commit()
cursor.close()
con.close()

