import streamlit as st
import json

def mostrar_panel_categorias():
    with open('./CP/output.json', 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
    
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