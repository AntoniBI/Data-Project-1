import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt
from precio_vivienda_stream import load_precios_vivienda, filtrar_distritos_por_precio
from hospitales_stream import get_hospitales_data, calcular_puntuacion_hospitales
from distritos_stream import load_distritos
from estaciones_stream import get_estaciones_data, calcular_puntuacion_estaciones
from educativos_stream import get_educativos_data, calcular_puntuacion_educativos


def calcular_color(distrito_id, top_distritos, cumple_precio):
    """
    Asigna el color a los distritos según los criterios:
    - Verde más oscuro para el mejor distrito.
    - Verde medio para el segundo mejor distrito.
    - Verde más claro para el tercer mejor distrito.
    - Verde genérico para distritos que cumplen el filtro de precio pero no están en el top 3.
    - Gris para distritos que no cumplen el filtro de precio.
    """
    if distrito_id in top_distritos:
        rank = top_distritos.index(distrito_id)
        colores_top = [
            [0, 128, 0, 150], 
            [0, 200, 0, 150],  
            [0, 255, 0, 150],  
        ]
        return colores_top[rank]
    elif cumple_precio:
        return [144, 238, 144, 150]  
    else:
        return [169, 169, 169, 100]  


def main():
    st.title("Mapa por Distritos en Valencia")

    # Cargar datos de distritos
    distritos_data = load_distritos()

    # Filtro de precios
    st.sidebar.header("Filtrar por Precios de Vivienda")
    precio_min = st.sidebar.slider("Precio mínimo", min_value=500, max_value=4500, value=1150, step=25)
    precio_max = st.sidebar.slider("Precio máximo", min_value=500, max_value=4500, value=1200, step=25)

    # Validación del rango de precios
    if precio_min > precio_max:
        st.sidebar.error("El precio mínimo no puede ser mayor que el precio máximo. Ajusta los valores.")
        st.stop()

    precios_data = load_precios_vivienda()
    precios_filtrados = filtrar_distritos_por_precio(precios_data, precio_min, precio_max)

    # Filtros segun importancia de hospitales, estaciones y centros educativos
    st.sidebar.header("Otros datos de interés")
    importancia_hospitales = st.sidebar.selectbox("¿Son muy importantes los centros sanitarios?",["Muy poca importancia", "Poca importancia", "Importancia media", "Importancia alta"])
    importancia_estaciones = st.sidebar.selectbox("¿Son muy importantes las estaciones de transporte publico?",["Muy poca importancia", "Poca importancia", "Importancia media", "Importancia alta"])
    importancia_educativos = st.sidebar.selectbox( "¿Son muy importantes los centros educativos?",["Muy poca importancia", "Poca importancia", "Importancia media", "Importancia alta"])
    
    hospitales_data = get_hospitales_data()
    hospitales_data = calcular_puntuacion_hospitales(hospitales_data, importancia_hospitales)

    estaciones_data = get_estaciones_data()
    estaciones_data = calcular_puntuacion_estaciones(estaciones_data, importancia_estaciones)
 
    educativos_data = get_educativos_data()
    educativos_data = calcular_puntuacion_educativos(educativos_data, importancia_educativos)

    # Combinar datos
    distritos_data = distritos_data.merge(precios_filtrados, on="district_id", how="left")
    distritos_data = distritos_data.merge(hospitales_data, on="district_id", how="left")
    distritos_data = distritos_data.merge(estaciones_data, on="district_id", how="left")
    distritos_data = distritos_data.merge(educativos_data, on="district_id", how="left")

    # # Reemplazar valores NaN en las columnas de puntuaciones con 0
    # distritos_data["puntuacion_hospitales"].fillna(0, inplace=True)
    # distritos_data["puntuacion_estaciones"].fillna(0, inplace=True)
    # distritos_data["puntuacion_educativos"].fillna(0, inplace=True)

    # Calcular puntuación total (hospitales + estaciones + educativos)
    distritos_data["puntuacion_total"] = (
        distritos_data["puntuacion_hospitales"] +
        distritos_data["puntuacion_estaciones"] +
        distritos_data["puntuacion_educativos"]
    )

    # Filtrar distritos que cumplen con el rango de precios
    distritos_filtrados = distritos_data[
        (distritos_data["precio_medio"] >= precio_min) &
        (distritos_data["precio_medio"] <= precio_max)
    ]

    # Seleccionar los 3 distritos con mayor puntuación total
    top_distritos = distritos_filtrados.nlargest(3, "puntuacion_total")["district_id"].tolist()

    # Configurar el color del mapa
    distritos_data["color"] = distritos_data.apply(
        lambda row: calcular_color(
            row["district_id"],
            top_distritos,
            row["precio_medio"] >= precio_min and row["precio_medio"] <= precio_max
        ),
        axis=1
    )

    # Crear capa GeoJson
    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        data=distritos_data,
        get_fill_color="color",
        get_line_color=[0, 0, 0, 200],
        line_width_min_pixels=1,
        pickable=True,
    )

    # Configuración del mapa
    view_state = pdk.ViewState(
        latitude=39.4699,
        longitude=-0.3763,
        zoom=11,
        pitch=0
    )

    # Estilo de Mapbox
    mapbox_style = "mapbox://styles/mapbox/streets-v11"

    # Tooltip del mapa
    tooltip = {
        "html": """
        <b>Distrito:</b> {nombre_distrito}<br>
        <b>Codigo de Distrito:</b> {district_id}<br>
        <b>Centros Sanitarios:</b> {total_hospitales}<br>
        <b>Estaciones Transporte Publico:</b> {total_stops}<br>
        <b>Centros Educativos:</b> {total_centros_educativos}
        """,
        "style": {"backgroundColor": "white", "color": "black"}
    }

    # Mostrar mapa
    r = pdk.Deck(
        layers=[geojson_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style=mapbox_style  
    )
    st.pydeck_chart(r)

    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.markdown("<div style='background-color:#008000;width:20px;height:20px;display:inline-block'></div> Mejor distrito", unsafe_allow_html=True)
        col2.markdown("<div style='background-color:#00C800;width:20px;height:20px;display:inline-block'></div> Segundo mejor distrito", unsafe_allow_html=True)
        col3.markdown("<div style='background-color:#00FF00;width:20px;height:20px;display:inline-block'></div> Tercer mejor distrito", unsafe_allow_html=True)
        col4.markdown("<div style='background-color:#90EE90;width:20px;height:20px;display:inline-block'></div> Cumple precio establecido", unsafe_allow_html=True)
        col5.markdown("<div style='background-color:#A9A9A9;width:20px;height:20px;display:inline-block'></div> No cumple precio establecido", unsafe_allow_html=True)

    st.subheader("Nuestras recomendaciones")
    if top_distritos:
        nombres_top = distritos_filtrados[distritos_filtrados["district_id"].isin(top_distritos)]["nombre_distrito"].unique()
        st.write("Basándonos en tus preferencias, te recomendamos vivir en los siguientes distritos:")
        for nombre in nombres_top:
            st.write(f"- {nombre}")
    else:
        st.write("No se encontraron distritos recomendados según tus preferencias.")

    # Crear el gráfico donde muestre el precio medio de vivienda, precio mínimo y precio máximo
    st.subheader("Precio medio de viviendas para tu selección")
    if not distritos_filtrados.empty:
        plt.figure(figsize=(10, 5))
        distritos_unicos = distritos_filtrados.drop_duplicates(subset=["nombre_distrito"])
        plt.plot(distritos_unicos["nombre_distrito"], distritos_unicos["precio_medio"], marker='o', label="Precio Medio")
        plt.plot(distritos_unicos["nombre_distrito"], distritos_unicos["precio_min"], linestyle='dashed', label="Precio Mínimo")
        plt.plot(distritos_unicos["nombre_distrito"], distritos_unicos["precio_max"], linestyle='dashed', label="Precio Máximo")
        plt.xlabel("Distrito")
        plt.ylabel("Precio (€)")
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        st.pyplot(plt)
    else:
        st.write("No hay distritos que cumplan con el rango de precios seleccionado.")


    st.subheader("Infraestructura en los distritos dentro del rango de precio")
    if not distritos_filtrados.empty:
    # Eliminar duplicados en los distritos, si los hay
        distritos_unicos = distritos_filtrados.drop_duplicates(subset=["district_id"])
    
    # Crear el gráfico para todos los distritos dentro del rango de precios
        fig, ax = plt.subplots(figsize=(12, 6))  # Aumentar el tamaño de la figura para más espacio
        distritos_unicos.plot(x="nombre_distrito", y=["total_hospitales", "total_stops", "total_centros_educativos"], kind="bar", ax=ax)
    
    # Rotar las etiquetas del eje X
        plt.xticks(rotation=45, ha="right", fontsize=10)
    
    # Etiquetas y leyenda
        plt.xlabel("Distrito")
        plt.ylabel("Cantidad")
        plt.legend(["Centros Sanitarios", "Estaciones Transporte Publico", "Centros Educativos"], fontsize="small")
    
    # Ajuste para evitar que las etiquetas se corten
        plt.tight_layout()

        st.pyplot(fig)
    else:
        st.write("No se encontraron distritos dentro del rango de precios seleccionado.")



    # Mostrar los 3 mejores distritos con sus detalles 

    st.subheader("Detalles de los 3 mejores distritos")
    if top_distritos:

    # Filtrar solo los distritos top y eliminar duplicados
        top_data = distritos_filtrados[distritos_filtrados["district_id"].isin(top_distritos)].drop_duplicates(subset=["district_id"])
    
    
        for _, distrito in top_data.iterrows():
            nombre_distrito = distrito["nombre_distrito"]
            precio_medio = distrito["precio_medio"]
            total_hospitales = distrito["total_hospitales"]
            total_estaciones = distrito["total_stops"]
            total_educativos = distrito["total_centros_educativos"]
        
            st.write(f"### {nombre_distrito}")
            st.write(f"  - **Precio Medio de Vivienda**: {precio_medio:,.2f} €")
            st.write(f"  - **Centros Sanitarios**: {total_hospitales}")
            st.write(f"  - **Estaciones de Transporte Público**: {total_estaciones}")
            st.write(f"  - **Centros Educativos**: {total_educativos}")
            st.write("---")
    else:
        st.write("No se encontraron distritos recomendados según tus preferencias.")



if __name__ == "__main__":
    main()
