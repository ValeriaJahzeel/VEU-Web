import streamlit as st
import folium
from streamlit_folium import folium_static

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