import streamlit as st
from components.mapa_categorias import mostrar_panel_categorias
from components.mapa_categorias import mostrar_mapa

def mostrar_mapa_y_filtros():
    """Muestra la sección del mapa y los filtros laterales"""
    # Crear 3 columnas para la sección
    col1, col2, col3 = st.columns([1, 2, 1])

    # Columna 1: Categorías
    with col1:
        mostrar_panel_categorias()

    # Columna 2: Mapa
    with col2:
        mostrar_mapa()

    # Columna 3: Filtro por CP
    with col3:
        mostrar_filtro_cp()

def mostrar_filtro_cp():
    """Muestra el panel de filtro por código postal"""
    st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
    st.markdown("<h3>Filtrar por CP</h3>", unsafe_allow_html=True)
    codigo_postal = st.text_input("Ingresa el código postal")
    st.markdown("</div>", unsafe_allow_html=True)