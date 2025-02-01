import os
import time
import subprocess

print("Iniciando servicios previos...")
# Simular espera o inicializar servicios (puedes agregar comandos aquí)
time.sleep(60)

print("Ejecutando Streamlit...")
subprocess.run(["streamlit", "run", "main.py", "--server.address=0.0.0.0"])

