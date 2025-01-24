# 

import pymongo
import psycopg2

# Conexión a MongoDB
myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017")
mydb = myclient["dataproject1"]
mycol = mydb["hospitales"]

# Conexión a PostgreSQL
conn = psycopg2.connect(
    user="postgres",
    password="Welcome01",
    host="localhost",
    port=5432
)
cursor = conn.cursor()

# Crear tabla hospitales
cursor.execute("""
    CREATE TABLE IF NOT EXISTS public."hospitales" (
        nombre_hospital VARCHAR(255),
        district_id INTEGER NOT NULL,
        tipo_centro VARCHAR(255) NOT NULL
    );
""")

# Recorrer los documentos de MongoDB
for document in mycol.find():
    # Validar que las claves existan en el documento
    nombre_hospital = document.get('nombre')
    district_id = document.get('coddistrit')
    tipo_centro = document.get('tipo')

    if nombre_hospital and district_id and tipo_centro:
        # Insertar datos en la tabla
        cursor.execute("""
            INSERT INTO public."hospitales" (nombre_hospital, district_id, tipo_centro) 
            VALUES (%s, %s, %s);
        """, (nombre_hospital, district_id, tipo_centro))

# Guardar los cambios y cerrar las conexiones
conn.commit()
cursor.close()
conn.close()

# Mensaje de éxito
print("Datos insertados correctamente.")
