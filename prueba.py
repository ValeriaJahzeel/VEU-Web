import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
from PIL import Image
import requests
from io import BytesIO
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Reportes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        background-color: #1A4E8C;
        padding: 1rem;
        border-radius: 0px;
        margin-bottom: 1rem;
        text-align: left;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .category-card {
        background-color: #3E6FB9;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        text-align: center;
    }
    .count-box {
        background-color: #2C5AA0;
        border-radius: 25px;
        padding: 0.3rem 1rem;
        margin: 0.5rem;
        display: inline-block;
        font-weight: bold;
    }
    .icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    .sidebar-section {
        margin-bottom: 1.5rem;
    }
    .filter-box {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='main-header'>Dashboard</div>", unsafe_allow_html=True)

# Selector de tiempo
col_espaciador, col_selector = st.columns([3, 1])
with col_selector:
    periodo = st.selectbox(
        "Filtrar por periodo",
        ["Última semana", "Último mes", "Últimos 3 meses", "Todo"],
        index=0
    )

# Datos de ejemplo para las categorías
categorias_data = {
    "Baches": {"No resueltos": 52, "Resueltos": 10, "icon": "🚧"},
    "Banqueta en mal estado": {"No resueltos": 52, "Resueltos": 10, "icon": "🚶"},
    "Zona poco iluminada": {"No resueltos": 52, "Resueltos": 10, "icon": "💡"},
    "Basura en vía pública": {"No resueltos": 52, "Resueltos": 10, "icon": "🗑️"}
}

# Sección de categorías destacadas
st.markdown("<h3>Categorías destacadas</h3>", unsafe_allow_html=True)
cols = st.columns(len(categorias_data))

for idx, (categoria, datos) in enumerate(categorias_data.items()):
    with cols[idx]:
        st.markdown(f"""
        <div class='category-card'>
            <div class='icon'>{datos['icon']}</div>
            <h4>{categoria}</h4>
            <div>
                <span>No resueltos</span>
                <div class='count-box'>{datos['No resueltos']}</div>
            </div>
            <div>
                <span>Resueltos</span>
                <div class='count-box'>{datos['Resueltos']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Contenido principal dividido en dos columnas
col1, col2, col3 = st.columns([1, 2, 1])

# Columna 1: Categorías
with col1:
    st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
    st.markdown("<h3>Categorías</h3>", unsafe_allow_html=True)
    
    st.markdown("<h4>Servicios</h4>", unsafe_allow_html=True)
    st.markdown("<details open>", unsafe_allow_html=True)
    st.markdown("<summary>Agua</summary>", unsafe_allow_html=True)
    st.markdown("</details>", unsafe_allow_html=True)
    
    st.markdown("<details open>", unsafe_allow_html=True)
    st.markdown("<summary>Obras</summary>", unsafe_allow_html=True)
    st.checkbox("Baches")
    st.checkbox("Daño en instalaciones")
    st.checkbox("Agua sobre construcción")
    st.markdown("</details>", unsafe_allow_html=True)
    
    st.markdown("<details>", unsafe_allow_html=True)
    st.markdown("<summary>Urbanismo</summary>", unsafe_allow_html=True)
    st.markdown("</details>", unsafe_allow_html=True)
    
    st.markdown("<details>", unsafe_allow_html=True)
    st.markdown("<summary>Ecología</summary>", unsafe_allow_html=True)
    st.markdown("</details>", unsafe_allow_html=True)
    
    st.markdown("<details>", unsafe_allow_html=True)
    st.markdown("<summary>Residuos</summary>", unsafe_allow_html=True)
    st.markdown("</details>", unsafe_allow_html=True)
    
    st.markdown("<details>", unsafe_allow_html=True)
    st.markdown("<summary>Animal</summary>", unsafe_allow_html=True)
    st.markdown("</details>", unsafe_allow_html=True)
    
    st.markdown("<h4>Social</h4>", unsafe_allow_html=True)
    st.markdown("<h4>Prevención de delito</h4>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Columna 2: Mapa
with col2:
    # Crear un mapa base centrado en alguna ubicación de interés (ejemplo: Ciudad de México)
    m = folium.Map(location=[19.4326, -99.1332], zoom_start=13)
    
    # Agregar algunos marcadores de ejemplo
    folium.Marker([19.4326, -99.1332], popup="Reporte 1: Bache").add_to(m)
    folium.Marker([19.4396, -99.1400], popup="Reporte 2: Iluminación").add_to(m)
    folium.Marker([19.4250, -99.1250], popup="Reporte 3: Basura").add_to(m)
    
    # Mostrar el mapa
    folium_static(m, width=600)

# Columna 3: Filtro por CP
with col3:
    st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
    st.markdown("<h3>Filtrar por CP</h3>", unsafe_allow_html=True)
    codigo_postal = st.text_input("Ingresa el código postal")
    st.markdown("</div>", unsafe_allow_html=True)

# Sección de estadísticas
st.markdown("<h2 class='sub-header'>Estadísticas</h2>", unsafe_allow_html=True)

# Datos de ejemplo para las estadísticas
fechas = pd.date_range(end=datetime.now(), periods=30).tolist()
reportes_por_dia = pd.DataFrame({
    'fecha': fechas,
    'reportes': [10, 15, 7, 12, 20, 15, 8, 10, 15, 17, 22, 15, 12, 10, 8, 12, 15, 20, 18, 14, 12, 15, 17, 19, 22, 20, 15, 12, 10, 8]
})

fig = px.line(reportes_por_dia, x='fecha', y='reportes', 
              title='Reportes por día',
              labels={'fecha': 'Fecha', 'reportes': 'Número de reportes'})
st.plotly_chart(fig, use_container_width=True)

# Datos de ejemplo para tipos de reportes
tipos_reportes = pd.DataFrame({
    'tipo': ['Baches', 'Iluminación', 'Basura', 'Banquetas', 'Otros'],
    'cantidad': [120, 80, 60, 40, 20]
})

col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    fig_pie = px.pie(tipos_reportes, values='cantidad', names='tipo', 
                   title='Distribución de reportes por tipo')
    st.plotly_chart(fig_pie, use_container_width=True)

with col_grafico2:
    fig_bar = px.bar(tipos_reportes, x='tipo', y='cantidad', 
                    title='Cantidad de reportes por tipo',
                    labels={'tipo': 'Tipo de reporte', 'cantidad': 'Cantidad'})
    st.plotly_chart(fig_bar, use_container_width=True)