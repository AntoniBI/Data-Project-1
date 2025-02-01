import time
import subprocess

# Retrasar la ejecución (por ejemplo, 30 segundos)
print("Esperando 30 segundos antes de iniciar la carga de datos...")
time.sleep(30)

# Lista de scripts a ejecutar en orden
scripts = [
    "distritos.py",
    "precios_vivienda.py",
    "hospitales_norm.py",
    "estaciones_norm.py",
    "educativos_norm.py"
]

# Ejecutar cada script uno por uno
for script in scripts:
    print(f"Ejecutando {script}...")
    try:
        subprocess.run(["python", script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando {script}: {e}")
        exit(1)  # Salir con error si falla algún script

print("Carga de datos completada con éxito.")
