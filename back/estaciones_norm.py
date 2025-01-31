import pymongo
import psycopg2
import pandas as pd

myclient = pymongo.MongoClient("mongodb://root:example@mongo:27017")
mydb = myclient["dataproject1"]
mycol = mydb["estaciones"]


documents = list(mycol.find())
df = pd.DataFrame(documents)

# Agrupar datos por distrito y contar las estaciones totales
result_df = df.groupby('coddistrit').size().reset_index(name='total_stops')

# Convertir el distrito a entero
result_df['coddistrit'] = result_df['coddistrit'].astype(int)

# Normalizar la variable total_stops usando Min-Max Scaling
result_df['normalized_total_stops'] = (result_df['total_stops'] - result_df['total_stops'].min()) / \
                                      (result_df['total_stops'].max() - result_df['total_stops'].min())


con = psycopg2.connect(
    user="postgres",
    password="Welcome01",
    host="postgres",
    port=5432
)
cursor = con.cursor()

# Crear tabla de resultados o añadir columna si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS public."total_estaciones" (
        district_id INTEGER PRIMARY KEY,
        total_stops INTEGER NOT NULL,
        normalized_total_stops FLOAT
    );
""")

# Añadir columna normalized_total_stops si no existe
cursor.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1
            FROM information_schema.columns 
            WHERE table_name = 'total_estaciones' AND column_name = 'normalized_total_stops'
        ) THEN
            ALTER TABLE public."total_estaciones"
            ADD COLUMN normalized_total_stops FLOAT;
        END IF;
    END $$;
""")

for _, row in result_df.iterrows():
    cursor.execute("""
        INSERT INTO public."total_estaciones" (district_id, total_stops, normalized_total_stops) 
        VALUES (%s, %s, %s)
        ON CONFLICT (district_id) 
        DO UPDATE SET 
            total_stops = EXCLUDED.total_stops,
            normalized_total_stops = EXCLUDED.normalized_total_stops;
    """, (int(row['coddistrit']), int(row['total_stops']), float(row['normalized_total_stops'])))

con.commit()
cursor.close()
con.close()


