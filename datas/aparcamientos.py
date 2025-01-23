import pymongo
import psycopg2

# Conexión a MongoDB
myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017")
mydb = myclient["dataproject1"]
mycol = mydb["aparcamientos"]

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
    CREATE TABLE IF NOT EXISTS public."aparcamiento" (
        distrito VARCHAR(255),
        habitantes INTEGER NOT NULL,
        total INTEGER NOT NULL,
        libres INTEGER NOT NULL       
    );
""")

# Recorrer los documentos de MongoDB
for document in mycol.find():
    # Validar que las claves existan en el documento
    distrito = document.get('districte')
    habitantes = document.get('habitants')
    total = document.get('total')
    libres = document.get('lliures')

    if distrito and habitantes and total and libres:
        # Insertar datos en la tabla
        cursor.execute("""
            INSERT INTO public."aparcamiento" (distrito, habitantes, total, libres)
            VALUES (%s, %s, %s, %s);
        """, (distrito, habitantes, total, libres))

# Guardar los cambios y cerrar las conexiones
conn.commit()
cursor.close()
conn.close()

# Mensaje de éxito
print("Datos insertados correctamente.")

