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
3. MongoDB.
4. PostgreSQL.
5. Sistema operativo compatible: Windows, Linux o macOS.
