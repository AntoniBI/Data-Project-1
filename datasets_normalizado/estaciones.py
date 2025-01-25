import pymongo
import psycopg2
import pandas as pd

# Conexión a MongoDB
myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017")
mydb = myclient["dataproject1"]
mycol = mydb["estaciones"]

# Leer datos desde MongoDB y transformarlos a un DataFrame
data = list(mycol.find({}, {"_id": 0, "coddistrit": 1, "transporte": 1, "stop_id": 1, "stop_name": 1}))  # Seleccionar solo los campos necesarios
df = pd.DataFrame(data)

# Asegurarse de que las columnas necesarias existen y no tienen valores nulos
df = df.dropna(subset=["coddistrit", "transporte", "stop_id", "stop_name"])
df["coddistrit"] = df["coddistrit"].astype(int)  # Convertir el código de distrito a entero

# Agrupar por distrito y tipo de transporte (bus, metro) y contar las estaciones
totales_por_distrito_transporte = df.groupby(["coddistrit", "transporte"]).size().unstack(fill_value=0)

# Asegurarse de que la tabla tenga las columnas correctas (bus, metro) aunque no haya datos en alguna categoría
totales_por_distrito_transporte = totales_por_distrito_transporte.reindex(columns=["emt", "metrovlc"], fill_value=0)

# Crear una columna con la suma de estaciones de bus y metro por distrito
totales_por_distrito_transporte["total_estaciones_bus_metro"] = totales_por_distrito_transporte["emt"] + totales_por_distrito_transporte["metrovlc"]

# Resetear el índice para convertirlo en columnas
totales_por_distrito_transporte.reset_index(inplace=True)

# Conexión a PostgreSQL
conn = psycopg2.connect(
    user="postgres",
    password="Welcome01",
    host="localhost",
    port=5432
)
cursor = conn.cursor()

# Crear tabla para los totales de estaciones de bus y metro por distrito
cursor.execute("""
    CREATE TABLE IF NOT EXISTS public."estaciones_por_distrito" (
        district_id INTEGER PRIMARY KEY,
        total_estaciones_bus INTEGER NOT NULL,
        total_estaciones_metro INTEGER NOT NULL
    );
""")

# Insertar los totales por distrito y tipo de transporte en la base de datos
for _, row in totales_por_distrito_transporte.iterrows():
    cursor.execute("""
        INSERT INTO public."estaciones_por_distrito" (district_id, total_estaciones_bus, total_estaciones_metro)
        VALUES (%s, %s, %s)
        ON CONFLICT (district_id) DO UPDATE
        SET total_estaciones_bus = EXCLUDED.total_estaciones_bus,
            total_estaciones_metro = EXCLUDED.total_estaciones_metro;
    """, (int(row["coddistrit"]), int(row["emt"]), int(row["metrovlc"])))  # Convertir a int

# Guardar los cambios y cerrar las conexiones
conn.commit()
cursor.close()
conn.close()

# Mensaje de éxito
print("Totales por distrito (estaciones bus y metro) insertados correctamente.")
