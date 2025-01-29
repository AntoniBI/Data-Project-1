# **Data Project - README**

## 📋 **Descripción del Proyecto**
Este proyecto tiene como objetivo ofrecer una plataforma interactiva que ayude a los usuarios a identificar cuál es la zona más adecuada de Valencia para establecer su residencia, según sus necesidades. Para ello, se tienen en cuenta factores como la disponibilidad de centros sanitarios, plazas de aparcamiento, vulnerabilidad social de los barrios, precios de la vivienda y estaciones de transporte público. La herramienta permite explorar los distritos mediante un mapa interactivo, aplicar filtros específicos y consultar detalles sobre cada zona.

El sistema se basa en la extracción de datos desde APIs mediante NiFi, que luego se almacenan en una base de datos MongoDB. A continuación, los datos se procesan con Python y se migran a PostgreSQL. Finalmente, se utiliza la biblioteca Streamlit para desarrollar una aplicación interactiva y visual.

## ⚙️ **Funcionalidades Principales**
- **Mapa Dinámico**: Representación de los distritos con sus respectivas características.
- **Consulta de Información**: Visualización de datos tabulares sobre las características filtradas.
- **Procesamiento de Datos**: Obtención de datos de fuentes abiertas y almacenamiento en PostgreSQL.
- **Base de Datos Relacional**: Organización y gestión de los datos mediante PostgreSQL.
- **Portabilidad y Reproducibilidad**: Uso de Docker para garantizar que el entorno sea fácilmente replicable.

## 🛠️ **Requisitos Previos**
1. Tener instalados Docker y Docker Compose.
2. Apache NiFi.
3. Python
4. MongoDB.
5. PostgreSQL.
6. Sistema operativo compatible: Windows, Linux o macOS.

## 🧑‍💻 **Tecnologías y Herramientas Utilizadas**

### **Python**
- **pandas**: Para el análisis y transformación de datos.
- **psycopg2**: Para la conexión y transferencia de datos entre Python y PostgreSQL.
- **pymongo**: Para interactuar con la base de datos MongoDB.
- **Streamlit**: Para crear una interfaz web interactiva que permita visualizar y explorar los datos.

### **Bases de Datos**
- **MongoDB**: Base de datos NoSQL utilizada para almacenar datos extraídos desde APIs.
- **PostgreSQL con PostGIS**: PostgreSQL se utiliza como base de datos relacional para almacenar datos estructurados. La extensión **PostGIS** permite trabajar con datos espaciales.

### **Docker**
- Contenerización del entorno para garantizar reproducibilidad y facilitar la implementación.

### **Apache NiFi**
- Herramienta de integración utilizada para extraer datos desde la API pública y almacenarlos automáticamente en MongoDB. 

-