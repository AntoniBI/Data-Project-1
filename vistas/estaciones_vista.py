import pymongo
import psycopg2

# Conexión a MongoDB
myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017")
mydb = myclient["dataproject1"]
mycol = mydb["estaciones"]

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
    CREATE TABLE IF NOT EXISTS public."estaciones" (
        district_id INTEGER NOT NULL,
        transporte VARCHAR(255) NOT NULL,
        stop_id INTEGER NOT NULL,
        stop_name VARCHAR(255) NOT NULL
    );
""")

# Recorrer los documentos de MongoDB
for document in mycol.find():
    # Validar que las claves existan en el documento
    district_id = document.get('coddistrit')
    transporte = document.get('transporte')
    stop_id = document.get('stop_id')
    stop_name = document.get('stop_name')
   
    if district_id and transporte and stop_id and stop_name:
        # Insertar datos en la tabla
        cursor.execute("""
            INSERT INTO public."estaciones" (district_id, transporte, stop_id, stop_name) 
            VALUES (%s, %s, %s, %s);
        """, (district_id, transporte, stop_id, stop_name))

cursor.execute("""
    CREATE OR REPLACE VIEW public.estaciones_transporte AS
    SELECT 
        district_id, 
        transporte,
        COUNT(stop_id) as total_estaciones
    FROM public."estaciones"
    GROUP BY district_id,transporte
    ORDER BY district_id;
""")



# Guardar los cambios y cerrar las conexiones
conn.commit()
cursor.close()
conn.close()

# Mensaje de éxito
print("Datos insertados correctamente.")
