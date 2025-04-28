import streamlit as st
import folium
from streamlit_folium import folium_static

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

def mostrar_panel_categorias():
    """Muestra el panel de filtros de categorías"""
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

def mostrar_mapa():
    """Muestra el mapa interactivo"""
    # Crear un mapa base centrado en alguna ubicación de interés (ejemplo: Ciudad de México)
    m = folium.Map(location=[19.4326, -99.1332], zoom_start=13)
    
    # Agregar algunos marcadores de ejemplo
    folium.Marker([19.4326, -99.1332], popup="Reporte 1: Bache").add_to(m)
    folium.Marker([19.4396, -99.1400], popup="Reporte 2: Iluminación").add_to(m)
    folium.Marker([19.4250, -99.1250], popup="Reporte 3: Basura").add_to(m)
    
    # Mostrar el mapa
    folium_static(m, width=600)

def mostrar_filtro_cp():
    """Muestra el panel de filtro por código postal"""
    st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
    st.markdown("<h3>Filtrar por CP</h3>", unsafe_allow_html=True)
    codigo_postal = st.text_input("Ingresa el código postal")
    st.markdown("</div>", unsafe_allow_html=True)