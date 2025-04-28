import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Reportes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
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
        margin-bottom: 0;
        text-align: left;
    }
    .categories-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        background-color: #1A4E8C;
        padding: 1rem;
        border-radius: 0px;
        margin-top: 0;
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
    .stats-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .chart-title {
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: white;
    }
    div[data-testid="stVerticalBlock"] > div:has(>.main-header) {
        padding-bottom: 0 !important;
    }
    div[data-testid="stVerticalBlock"] > div:has(>.categories-header) {
        padding-top: 0 !important;
    }
    .reportes-section {
        margin-top: 2rem;
    }
    .map-container {
        padding: 0;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='main-header'>Dashboard</div>", unsafe_allow_html=True)

# Sección Categorías Destacadas
st.markdown("<div class='categories-header'>Categorías destacadas</div>", unsafe_allow_html=True)

# Selector de tiempo en la esquina superior derecha
col_espaciador, col_selector = st.columns([3, 1])
with col_selector:
    periodo = st.selectbox(
        "",
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

# Sección del mapa y categorías
col1, col2, col3 = st.columns([1, 2, 1])

# Columna 1: Categorías
with col1:
    st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
    st.markdown("<h3>Categorías</h3>", unsafe_allow_html=True)
    
    st.markdown("<h4>Servicios</h4>", unsafe_allow_html=True)
    st.markdown("<details>", unsafe_allow_html=True)
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
st.markdown("<h2 class='reportes-section'>Estadísticas</h2>", unsafe_allow_html=True)
st.markdown("<h3>Reportes por tipo</h3>", unsafe_allow_html=True)

# Datos de ejemplo para la gráfica de barras apiladas
meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
tipos_reportes = ['Baches', 'Basura', 'Iluminación', 'Banquetas', 'Otros']
colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Crear datos aleatorios para cada tipo de reporte
datos_por_tipo = {}
for tipo in tipos_reportes:
    base = np.random.randint(50, 100)
    datos_por_tipo[tipo] = [base + np.random.randint(-20, 30) for _ in range(len(meses))]

# Crear la gráfica de barras apiladas
fig_barras = go.Figure()

for i, tipo in enumerate(tipos_reportes):
    fig_barras.add_trace(go.Bar(
        x=meses,
        y=datos_por_tipo[tipo],
        name=tipo,
        marker_color=colores[i % len(colores)]
    ))

fig_barras.update_layout(
    barmode='stack',
    title='Reportes mensuales por tipo',
    xaxis_title='Mes',
    yaxis_title='Número de reportes',
    legend_title='Tipo de reporte',
    template='plotly_white',
    height=400,
    margin=dict(t=50, b=50, l=50, r=50)
)

# Mostrar la gráfica de barras apiladas en una tarjeta
st.markdown("<div class='stats-card'>", unsafe_allow_html=True)
st.plotly_chart(fig_barras, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sección de línea temporal
st.markdown("<h3>Línea temporal</h3>", unsafe_allow_html=True)

# Datos de ejemplo para la gráfica de líneas
fechas = pd.date_range(end=datetime.now(), periods=12, freq='M')
series_data = {
    'Total': [150, 120, 180, 200, 170, 220, 280, 230, 190, 250, 270, 220],
    'Resueltos': [100, 80, 120, 140, 110, 140, 210, 150, 120, 170, 180, 140],
    'Pendientes': [50, 40, 60, 60, 60, 80, 70, 80, 70, 80, 90, 80]
}

df_lineas = pd.DataFrame({
    'fecha': fechas,
    'Total': series_data['Total'],
    'Resueltos': series_data['Resueltos'],
    'Pendientes': series_data['Pendientes']
})

# Crear la gráfica de líneas
fig_lineas = go.Figure()

fig_lineas.add_trace(go.Scatter(
    x=df_lineas['fecha'],
    y=df_lineas['Total'],
    mode='lines+markers',
    name='Total',
    line=dict(color='#1f77b4', width=3)
))

fig_lineas.add_trace(go.Scatter(
    x=df_lineas['fecha'],
    y=df_lineas['Resueltos'],
    mode='lines+markers',
    name='Resueltos',
    line=dict(color='#2ca02c', width=3)
))

fig_lineas.add_trace(go.Scatter(
    x=df_lineas['fecha'],
    y=df_lineas['Pendientes'],
    mode='lines+markers',
    name='Pendientes',
    line=dict(color='#d62728', width=3)
))

fig_lineas.update_layout(
    title='Evolución de reportes a lo largo del tiempo',
    xaxis_title='Fecha',
    yaxis_title='Número de reportes',
    legend_title='Estado',
    template='plotly_white',
    height=400,
    margin=dict(t=50, b=50, l=50, r=50)
)

# Mostrar la gráfica de líneas en una tarjeta
st.markdown("<div class='stats-card'>", unsafe_allow_html=True)
st.plotly_chart(fig_lineas, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)