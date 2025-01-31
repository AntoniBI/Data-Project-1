# **Data Project - README**

## 📋 **Descripción del Proyecto**
Este proyecto tiene como objetivo ofrecer una plataforma interactiva que ayude a los usuarios a identificar cuál es la zona más adecuada de Valencia para establecer su residencia, según sus necesidades. Para ello, se consideran factores como la disponibilidad de centros sanitarios, centros educativos, precios de la vivienda y estaciones de transporte público. La herramienta permite explorar los distritos mediante un mapa interactivo, aplicar filtros específicos y consultar diversos detalles.

El sistema se basa en la extracción de datos desde APIs públicas mediante **Apache NiFi**, que luego se almacenan en una base de datos **MongoDB**. A continuación, los datos se procesan con **Python** y se migran a **PostgreSQL**. Finalmente, se utiliza la biblioteca **Streamlit** para desarrollar una aplicación interactiva y visual. Toda la aplicación está dockerrizada para garantizar portabilidad y facilidad de despliegue.

### **Estructura del Proyecto: Back-End y Front-End**
El proyecto está dividido en dos partes fundamentales:

#### **1. Back-End: Procesamiento de Datos y Gestión de Bases de Datos**
La parte **back-end** se encarga de recibir, procesar y almacenar los datos en la base de datos relacional **PostgreSQL**. Los datos provienen de diversas APIs, y inicialmente se almacenan en **MongoDB**.

**Flujo de Trabajo**:
1. **Recopilación de Datos**: Los datos se extraen desde diversas **APIs públicas** utilizando **Apache NiFi**, una herramienta de integración que automatiza la extracción y el almacenamiento de los datos en **MongoDB**.

2. **Transformación de los Datos**: Una vez almacenados en MongoDB, el back-end toma esos datos y los procesa mediante scripts en **Python**. Estos scripts realizan tareas de limpieza y transformación, convirtiendo los datos crudos en un formato estructurado adecuado para análisis posteriores. Además, se aplican reglas como la normalización y la geocodificación de distritos.

3. **Migración a PostgreSQL**: Después de la transformación, los datos se migran a **PostgreSQL**, una base de datos relacional que estructura la información de los distritos, incluyendo detalles como centros educativos, sanitarios, precios de vivienda, entre otros. La extensión **PostGIS** de PostgreSQL permite realizar análisis geoespaciales.

4. **Manejo de Datos Espaciales**: Al integrar **PostGIS**, el back-end es capaz de realizar consultas geoespaciales, lo que facilita obtener información sobre la extension de los distritos.

#### **2. Front-End: Interfaz Interactiva con Streamlit**
La parte **front-end** del proyecto está desarrollada utilizando **Streamlit**. Esta aplicación web interactiva permite a los usuarios explorar los datos de manera visual y personalizada.

**Características del Front-End**:
- **Mapa Dinámico**: Los distritos de Valencia son representados en un mapa interactivo. Los usuarios pueden aplicar filtros según sus preferencias (por ejemplo, importancia sobre la cantidad de centros educativos o sanitarios, rango de precios de vivienda, etc.), y el mapa se actualiza dinámicamente según los filtros aplicados.
- **Consulta de Información**: Los usuarios pueden ver los datos detallados de cada distrito, tales como los precios de la vivienda, la cantidad de centros educativos, sanitarios y estaciones. 
- **Interacción Visual**: La interfaz es intuitiva y fácil de usar. Los usuarios pueden ajustar los parámetros y explorar los datos según sus intereses.

El front-end se comunica con el back-end para obtener los datos procesados y presentarlos de manera atractiva y accesible.

## ⚙️ **Funcionalidades Principales**
- **Mapa Dinámico**: Visualización interactiva de los distritos de Valencia con filtros que permiten personalizar la experiencia del usuario. Los distritos se colorean según las preferencias, facilitando la búsqueda de la zona más adecuada para vivir.
- **Consulta de Información**: Visualización de datos que incluyen características relevantes de cada distrito, tales como la cantidad de centros educativos, centros sanitarios, estaciones de transporte público (EMT y Metrovalencia), y precios de vivienda.
- **Procesamiento de Datos**: Obtención, limpieza y transformación de datos desde diversas fuentes abiertas (APIs). La información se procesa y almacena en bases de datos estructuradas para ser utilizada por el front-end.
- **Base de Datos Relacional**: Uso de **PostgreSQL** para almacenar y gestionar los datos de cada distrito. La extensión **PostGIS** permite trabajar con información geoespacial, facilitando el análisis espacial y las consultas geográficas.
- **Portabilidad y Reproducibilidad**: El proyecto está dockerizado, lo que permite crear un entorno completamente aislado y reproducible, facilitando su implementación en diferentes entornos y su colaboración entre equipos.

## 🛠️ **Requisitos**
1. Tener instalados **Docker** y **Docker Compose** para contenerizar el entorno de desarrollo.
2. **Apache NiFi** para integrar y extraer los datos desde las APIs externas.
3. **Python** para procesar los datos y generar visualizaciones.
4. **MongoDB**: Base de datos NoSQL para almacenar los datos extraídos desde las APIs.
5. **PostgreSQL con PostGIS**: Base de datos relacional utilizada para almacenar y gestionar los datos procesados que se envían a **Streamlit**.

## 🧑‍💻 **Tecnologías y Herramientas Utilizadas**

### **Python**
- **pandas**: Biblioteca para el análisis y transformación de datos.
- **psycopg2**: Paquete para conectar y transferir datos entre Python y PostgreSQL.
- **pymongo**: Biblioteca que facilita la interacción con MongoDB desde Python.
- **Streamlit**: Framework para desarrollar aplicaciones web interactivas que permiten visualizar y explorar los datos de manera sencilla.
- **Pydeck**: Herramienta para crear visualizaciones interactivas, especialmente útil para mostrar datos geoespaciales.
- **matplotlib**: Biblioteca para crear gráficos estáticos y visualizaciones de datos.

### **Bases de Datos**
- **MongoDB**: Base de datos NoSQL utilizada para almacenar los datos crudos extraídos de las APIs públicas.
- **PostgreSQL con PostGIS**: Base de datos relacional que permite almacenar datos estructurados y realizar consultas complejas sobre datos geoespaciales.

### **Docker**
- Dockeriza el proyecto para asegurar que todos los componentes (NiFi, MongoDB, PostgreSQL, Streamlit) funcionen de manera consistente en cualquier entorno de desarrollo o producción.

### **Apache NiFi**
- Herramienta de integración que facilita la ingestión de datos desde diversas APIs públicas y su almacenamiento en MongoDB de manera automatizada.

### **Video Demo**




## 🚀 **Cómo Iniciar el Servicio**
1. Inicia los servicios principales ejecutando:
   ```bash
   docker compose up -d nifi mongo mongo-express postgres pgadmin
   ```
2. Accede a Apache NiFi en el navegador e importa el template correspondiente.
3. Inicia NiFi y permite que consuma únicamente un flowfile.
4. Detén NiFi una vez finalizado el proceso.
5. Levanta los contenedores del back y front con:
   ```bash
   docker compose up -d
   ```
6. Accede a la aplicación web en el navegador a través de:
   ```
   http://localhost:8501
   ```

