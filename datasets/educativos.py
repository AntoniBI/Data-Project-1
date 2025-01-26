import pymongo

# Relaciones entre código postal y distrito (añadidos los nuevos códigos postales para completar la relación)
data = {
    "codigo_postal": [
        46001, 46002, 46003, 46004, 46005, 46006, 46007, 46008, 46009, 46010, 46011, 46012,
        46013, 46014, 46015, 46016, 46017, 46018, 46019, 46020, 46022, 46023, 46024, 46026,
        46035, 46112, 46100, 46113, 46120, 46021, 46025, 46920
    ],
    "codigo_distrito": [
        1, 1, 1, 2, 2, 2, 3, 3, 5, 5, 11, 19,
        10, 7, 4, 16, 9, 7, 15, 13, 12, 10, 12, 10,
        17, 17, 18, 18, 18, 19, 20, 21
    ]
}

# Conexión a MongoDB
myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017")
mydb = myclient["dataproject1"]
mycol = mydb["educativos"]

# Crear una lista con todos los códigos postales
todos_codpos = [int(document.get('codpos')) for document in mycol.find() if document.get('codpos')]

# Crear una lista con el código postal, su frecuencia y el distrito
codpos_count = []
if todos_codpos:  # Verificar que la lista no esté vacía
    for codpos in set(todos_codpos):
        frecuencia = todos_codpos.count(codpos)
        if codpos in data["codigo_postal"]:
            index = data["codigo_postal"].index(codpos)
            district_id = data["codigo_distrito"][index]
            codpos_count.append([codpos, frecuencia, district_id])
        else:
            codpos_count.append([codpos, frecuencia, None])  # Agregar None si no hay distrito asociado

# Imprimir la lista
if codpos_count:
    for item in codpos_count:
        if item[2] is None:
            print(f"Código Postal: {item[0]}, Frecuencia: {item[1]}, Distrito: No asignado")
        else:
            print(f"Código Postal: {item[0]}, Frecuencia: {item[1]}, Distrito: {item[2]}")
else:
    print("No se encontraron datos para generar la lista.")

# Mensaje de éxito
print("Lista generada correctamente.")