
import pymongo
import psycopg2

# Conexión a MongoDB
myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017")
mydb = myclient["dataproject1"]
mycol = mydb["vulnerabilidad"]

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
    CREATE TABLE IF NOT EXISTS public."vulnerabilidad_barrios" (
        distrito VARCHAR(255),
        indice_equipamiento VARCHAR(255),
        vulnerabilidad_equipamiento VARCHAR(255),
        indice_demografico VARCHAR(255),
        vulnerabilidad_demografica VARCHAR(255),
        indice_economico VARCHAR(255),
        vulnerabilidad_economica VARCHAR(255),
        indice_global VARCHAR(255),
        vulnerabilidad_global VARCHAR(255)
        
    );
""")

# Recorrer los documentos de MongoDB
for document in mycol.find():
    # Validar que las claves existan en el documento
    distrito = document.get('distrito')
    indice_equipamiento = document.get('ind_equip')
    vulnerabilidad_equipamiento = document.get('vul_equip')
    indice_demografico = document.get('ind_dem')
    vulnerabilidad_demografica = document.get('vul_dem')
    indice_economico = document.get('ind_econom')
    vulnerabilidad_economica = document.get('vul_econom')
    indice_global = document.get('ind_global')
    vulnerabilidad_global = document.get('vul_global')

    if distrito and indice_equipamiento and vulnerabilidad_equipamiento and indice_demografico and vulnerabilidad_demografica and indice_economico and vulnerabilidad_economica and indice_global and vulnerabilidad_global:
        # Insertar datos en la tabla
        cursor.execute("""
            INSERT INTO public."vulnerabilidad_barrios" (distrito, indice_equipamiento, vulnerabilidad_equipamiento, indice_demografico, vulnerabilidad_demografica, indice_economico, vulnerabilidad_economica, indice_global, vulnerabilidad_global) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (distrito, indice_equipamiento, vulnerabilidad_equipamiento, indice_demografico, vulnerabilidad_demografica, indice_economico, vulnerabilidad_economica, indice_global, vulnerabilidad_global))

# Guardar los cambios y cerrar las conexiones
conn.commit()
cursor.close()
conn.close()

# Mensaje de éxito
print("Datos insertados correctamente.")

