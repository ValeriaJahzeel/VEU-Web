import streamlit as st
from utils.styles import apply_styles
from components.header import create_header
from components.categorias_destacadas import mostrar_categorias_destacadas
from components.mapa_filtros import mostrar_mapa_y_filtros
from components.estadisticas import mostrar_estadisticas

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Reportes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Aplicar estilos CSS
apply_styles()

# Header
create_header()

# Sección de categorías destacadas
mostrar_categorias_destacadas()

# Sección del mapa y filtros
mostrar_mapa_y_filtros()

# Sección de estadísticas
mostrar_estadisticas()