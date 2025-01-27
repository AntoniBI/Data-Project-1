#Instalamos la imagen de python 3.10 en version slim para reducir el tamaño de la imagen
FROM python:3.11-slim

#Establecemos el directorio de trabajo
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#Copiamos el archivo requirements.txt a la imagen para instalar las dependencias
COPY requirements.txt ./

#Instalamos las dependencias
RUN pip install -r requirements.txt

#Copiamos todo el contenido de la carpeta actual a la imagen
COPY . .

#Exponemos el puerto 8501. Puerto nativo de streamlit
EXPOSE 8501

#Ejecutamos el comando streamlit run para correr la aplicación
CMD ["bash", "-c", "cd /app/streamlit && streamlit run main.py"]