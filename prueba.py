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

# Crear tabla aparcamientos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS public."aparcamiento2" (
        distrito VARCHAR(255) PRIMARY KEY,
        habitantes INTEGER NOT NULL,
        libres INTEGER NOT NULL       
    );
""")

# Usar un conjunto para almacenar distritos únicos
distritos_procesados = set()

# Recorrer los documentos de MongoDB
for document in mycol.find():
    # Validar que las claves existan en el documento
    distrito = document.get('districte')
    habitantes = document.get('habitants')
    libres = document.get('lliures')

    # Comprobar si el distrito ya se procesó
    if distrito and distrito not in distritos_procesados:
        # Comprobar si los datos necesarios existen
        if habitantes is not None and libres is not None:
            # Insertar datos en la tabla
            cursor.execute("""
                INSERT INTO public."aparcamiento" (distrito, habitantes, libres)
                VALUES (%s, %s, %s)
                ON CONFLICT (distrito) DO NOTHING;
            """, (distrito, habitantes, libres))

            # Añadir el distrito al conjunto de procesados
            distritos_procesados.add(distrito)

# Guardar los cambios y cerrar las conexiones
conn.commit()
cursor.close()
conn.close()

# Mensaje de éxito
print("Datos insertados correctamente.")
