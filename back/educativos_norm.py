import pymongo
import psycopg2

# Relaciones entre código postal y distrito
data = {
    "codigo_postal": [
        46001, 46002, 46003, 46004, 46005, 46006, 46007, 46008, 46009, 46010, 46011, 46012,
        46013, 46014, 46015, 46016, 46017, 46018, 46019, 46020, 46022, 46023, 46024, 46026,
        46035, 46112, 46100, 46113, 46120, 46021, 46025, 46920, 46018, 46010, 46020
    ],
    "codigo_distrito": [
        1, 1, 1, 2, 2, 2, 3, 3, 5, 5, 11, 19,
        10, 7, 4, 16, 9, 7, 15, 13, 12, 10, 12, 10,
        17, 17, 18, 18, 18, 19, 20, 21, 8, 6, 14
    ]
}

myclient = pymongo.MongoClient("mongodb://root:example@mongo:27017")
mydb = myclient["dataproject1"]
mycol = mydb["educativos"]

# Crear una lista con todos los códigos postales
todos_codpos = [int(document.get('codpos')) for document in mycol.find() if document.get('codpos')]

# Crear una lista con el código postal y el distrito
codpos_count = []
if todos_codpos:
    for codpos in set(todos_codpos):
        frecuencia = todos_codpos.count(codpos)
        if codpos in data["codigo_postal"]:
            index = data["codigo_postal"].index(codpos)
            district_id = data["codigo_distrito"][index]
            codpos_count.append([codpos, frecuencia, district_id])
        else:
            codpos_count.append([codpos, frecuencia, None])

# Sumar las frecuencias por distrito
district_frequencies = {}
for item in codpos_count:
    district_id = item[2]
    if district_id is not None:
        if district_id in district_frequencies:
            district_frequencies[district_id] += item[1]
        else:
            district_frequencies[district_id] = item[1]

# Añadir valores por defecto para los distritos que faltan
default_values = {8: 26, 6: 23, 14: 21}  
for district_id, default_value in default_values.items():
    if district_id not in district_frequencies:
        district_frequencies[district_id] = default_value

# Encontrar la frecuencia máxima entre los distritos
frecuencia_max = max(district_frequencies.values())

# Crear una tabla normalizada por distrito
district_normalized = []
for district_id, total_frecuencia in district_frequencies.items():
    normalized_frequency = round(total_frecuencia / frecuencia_max, 2)
    district_normalized.append([district_id, total_frecuencia, normalized_frequency])


con = psycopg2.connect(
    user="postgres",
    password="Welcome01",
    host="postgres",
    port=5432
)
cursor = con.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS public."centros_educativos" (
        district_id INTEGER PRIMARY KEY,
        total_centros_educativos INTEGER NOT NULL,
        normalized_total_centros_educativos FLOAT
    );
""")

for item in district_normalized:
    cursor.execute("""
        INSERT INTO public."centros_educativos" (district_id, total_centros_educativos, normalized_total_centros_educativos)
        VALUES (%s, %s, %s)
        ON CONFLICT (district_id) DO UPDATE
        SET total_centros_educativos = EXCLUDED.total_centros_educativos,
            normalized_total_centros_educativos = EXCLUDED.normalized_total_centros_educativos;
    """, (item[0], item[1], item[2]))

con.commit()
cursor.close()
con.close()


