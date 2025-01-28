import pandas as pd
import psycopg2

# Crear la tabla en pandas
data = {
    "codigo_postal": [
        46001, 46002, 46003, 46004, 46005, 46006, 46006, 46006, 46007, 46007, 46008, 46009,
        46010, 46010, 46011, 46012, 46013, 46014, 46014, 46015, 46015, 46016, 46016, 46017,
        46017, 46018, 46018, 46019, 46019, 46020, 46020, 46022, 46022, 46023, 46023, 46023,
        46024, 46024, 46026, 46026, 46035, 46035, 46112, 46131
    ],
    "nombre_distrito": [
        "Ciutat Vella", "Ciutat Vella", "Ciutat Vella", "Eixample", "Eixample", "Eixample", "Patraix", "Jesús",
        "Extramurs", "Jesús", "Extramurs", "La Saïdia", "La Saïdia", "El Pla del Real", "Poblats Marítims",
        "Pobles del Sud", "Quatre Carreres", "L'Olivereta", "Patraix", "Campanar", "Benicalap", "Benicalap",
        "Pobles del Nord", "Jesús", "Patraix", "L'Olivereta", "Patraix", "Rascanya", "La Saïdia", "Algirós",
        "Benimaclet", "Camins al Grau", "Algirós", "Quatre Carreres", "Algirós", "Camins al Grau", "Camins al Grau",
        "Poblats Marítims", "Quatre Carreres", "Pobles del Sud", "Pobles del Nord", "Pobles de l'Oest", "Pobles del Nord",
        "Pobles del Nord"
    ],
    "codigo_distrito": [
        1, 1, 1, 2, 2, 2, 8, 9, 3, 9, 3, 5, 5, 6, 11, 19, 10, 7, 8, 4, 16, 16, 17, 9, 8, 7, 8, 15, 5, 13, 14, 12, 13, 10,
        13, 12, 12, 11, 10, 19, 17, 18, 17, 17
    ]
}

df = pd.DataFrame(data)

# Conexión a PostgreSQL
conn = psycopg2.connect(
    user="postgres",
    password="Welcome01",
    host="localhost",
    port=5432,
    database="postgres"
)
cursor = conn.cursor()

# Crear tabla en la base de datos con clave primaria
cursor.execute("""
    CREATE TABLE IF NOT EXISTS public."distritos_valencia" (
        codigo_postal INTEGER PRIMARY KEY,
        nombre_distrito TEXT,
        codigo_distrito INTEGER
    );
""")

# Insertar los datos en la tabla
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO public."distritos_valencia" (codigo_postal, nombre_distrito, codigo_distrito)
        VALUES (%s, %s, %s)
        ON CONFLICT (codigo_postal) DO UPDATE
        SET nombre_distrito = EXCLUDED.nombre_distrito,
            codigo_distrito = EXCLUDED.codigo_distrito;
    """, (int(row["codigo_postal"]), row["nombre_distrito"], int(row["codigo_distrito"])))

# Guardar los cambios y cerrar la conexión
conn.commit()
cursor.close()
conn.close()

# Mensaje de éxito
print("Datos insertados correctamente en la tabla distritos_valencia.")
