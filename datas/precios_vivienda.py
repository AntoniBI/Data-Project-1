import pymongo
import psycopg2

# Conexión a MongoDB
myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017")
mydb = myclient["dataproject1"]
mycol = mydb["preciosviv"]

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
    CREATE TABLE IF NOT EXISTS public."precio_vivienda" (
        precio_m2 VARCHAR(255),
        district_id INTEGER NOT NULL
    );
""")

# Recorrer los documentos de MongoDB
for document in mycol.find():
    # Validar que las claves existan en el documento
    precio_m2 = document.get('precio_2022_euros_m2')
    district_id = document.get('coddistrit')
   

    if precio_m2 and district_id:
        # Insertar datos en la tabla
        cursor.execute("""
            INSERT INTO public."precio_vivienda"(precio_m2, district_id) 
            VALUES (%s, %s);
        """, (precio_m2, district_id))

# Guardar los cambios y cerrar las conexiones
conn.commit()
cursor.close()
conn.close()

# Mensaje de éxito
print("Datos insertados correctamente.")
