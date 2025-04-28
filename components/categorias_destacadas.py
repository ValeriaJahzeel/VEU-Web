import streamlit as st
from utils.data import obtener_datos_categorias

def mostrar_categorias_destacadas():
    """Muestra la sección de categorías destacadas"""
    # Sección Categorías Destacadas con título
    st.markdown("<div class='categories-header'>Categorías destacadas</div>", unsafe_allow_html=True)

    # Selector de tiempo en la esquina superior derecha
    col_espaciador, col_selector = st.columns([3, 1])
    with col_selector:
        periodo = st.selectbox(
            "",
            ["Última semana", "Último mes", "Últimos 3 meses", "Todo"],
            index=0
        )

    # Obtener datos de las categorías
    categorias_data = obtener_datos_categorias()

    # Crear columnas para las tarjetas
    cols = st.columns(len(categorias_data))

    # Mostrar tarjetas de categorías
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