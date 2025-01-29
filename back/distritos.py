import pymongo
import psycopg2
import json

# Conexión a MongoDB
myclient = pymongo.MongoClient("mongodb://root:example@mongo:27017")
mydb = myclient["dataproject1"]
mycol = mydb["distritos"]

# Conexión a PostgreSQL
conn = psycopg2.connect(
    user="postgres",
    password="Welcome01",
    host="postgres",
    port=5432
)
cursor = conn.cursor()

# Crear tabla hospitales
cursor.execute("""
    CREATE TABLE IF NOT EXISTS public."distritos" (
        nombre_distrito VARCHAR(255),
        district_id INTEGER NOT NULL,
        geo_shape geometry
    );
""")

# Recorrer los documentos de MongoDB
for document in mycol.find():
    # Validar que las claves existan en el documento
    nombre_distrito = document.get('nombre')
    district_id = document.get('coddistrit')
    geo_shape = document.get("geo_shape", {}).get("geometry", None)
    
    #Procesar el geo_shape
    geojson_str = json.dumps(geo_shape) if geo_shape else None
    point_wkt = None

    if nombre_distrito and district_id and geo_shape:
        # Insertar datos en la tabla
        cursor.execute("""
            INSERT INTO public."distritos" (nombre_distrito, district_id, geo_shape) 
            VALUES (%s, %s,ST_GeomFromGeoJSON(%s));
        """, (nombre_distrito, district_id, geojson_str))

# Guardar los cambios y cerrar las conexiones
conn.commit()
cursor.close()
conn.close()

# Mensaje de éxito
print("✅ Datos cargados correctamente a PostgreSQL")
