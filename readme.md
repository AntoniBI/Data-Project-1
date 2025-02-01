# **Data Project - README**

## 📅 **Cronograma**
- **1 semana para dudas de negocio**: Durante esta semana podrás plantear preguntas relacionadas con la lógica de negocio. Las dudas estarán abiertas para todos los integrantes del equipo.
- **Restricción en preguntas técnicas**: Las consultas tecnológicas están permitidas, pero recibirán una penalización. La ponderación será:
  - **60% Tecnología**
  - **40% Negocio**
- **Fechas clave**:
  - **9 de enero**: Publicación oficial del proyecto "Data Project".
  - **20 de enero**: Fecha límite para resolver dudas sobre aspectos técnicos y de negocio.
  - **1 de febrero**: Entrega final del proyecto.

> **Nota**: Es obligatorio realizar una presentación para exponer el proyecto.

## 🧩 **Aspectos a Evaluar**

### **Negocio**
Se valorará principalmente:
- **Originalidad**: La creatividad e innovación en la solución propuesta.
- **Adecuación**: Qué tan bien responde la solución a las necesidades planteadas.
- **Viabilidad**: La posibilidad real de implementar la solución.

### **Tecnología**
En el apartado técnico se evaluará:
- **Arquitectura**: Diseño estructural del sistema y sus componentes.
- **Idoneidad de las decisiones**: Explicación y defensa de las elecciones tecnológicas realizadas.

## 🌍 **Contexto del Proyecto**
En respuesta a los recientes acontecimientos de la DANA, el objetivo es ayudar a los ciudadanos de Valencia a determinar cuál sería la mejor zona para residir. **Las zonas afectadas por inundaciones no tienen por qué influir directamente en la elección.**

El proyecto debe centrarse en:
- **Seleccionar un distrito de Valencia o del área metropolitana** ideal para vivir. 
- Evaluar las zonas según diferentes criterios, como:
  - Aspectos económicos.
  - Factores geográficos.
  - Proximidad a escuelas u otros servicios.
  - Calidad de vida en general.

## 🛠️ **Restricciones Técnicas**
1. **Tecnología vista en clase**: Es obligatorio utilizar las herramientas y metodologías aprendidas durante el curso.
2. **Prohibido usar servicios en la nube (Cloud)**.
3. **Uso obligatorio de Streamlit**:
   - La solución debe incluir una aplicación interactiva desarrollada en Python con la biblioteca **Streamlit**.
4. **Dockerización**:
   - Todo el proyecto debe ser **dockerizable**.
   - Se debe incluir un archivo **Docker Compose** para desplegar fácilmente el entorno del proyecto.
   - La única excepción a esta regla es **Tableau**.

## 📦 **Entregables**
Para que el proyecto sea considerado completo, debe incluir los siguientes elementos:
1. **Diseño de la arquitectura**: Un esquema claro que explique la estructura y componentes del sistema.
2. **Datasets utilizados**: Los datos trabajados deben ser entregados en formato legible y reproducible.
3. **Docker**: Configuración lista para ejecutar el proyecto mediante Docker Compose.
4. **Repositorio en GitHub**: Un repositorio público o privado que contenga todo el código y los recursos del proyecto.
5. **Video de demostración**:
   - Es recomendable incluir un video explicativo que muestre el funcionamiento de la aplicación como una demo práctica.

## 🌐 **Uso de APIs**
Es obligatorio utilizar datos de APIs públicas 

## 🔄 **Jornadas de Trabajo**
Habrá una jornada de trabajo 

### **Integrantes del Proyecto**
- Juan
- Antoni
- Miguel

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
Enlace al video subido a Youtube: https://youtu.be/pNk8_3xJnwE

### **Presentación para la defensa del Data Project en clase**
Enlace a la presentacón en Figma: https://www.figma.com/deck/F0fsSuYYpfBUCfjwpivBjW/Data-Project-1?node-id=11-140&t=OwWcRi27WVTH8v9L-1

## 🚀 **Cómo Iniciar el Servicio**
1. Inicia los servicios con docker compose up -d
2. Accede a la aplicación de Streamlit copiando esta dirección en tu explorador de internet http://localhost:8501

