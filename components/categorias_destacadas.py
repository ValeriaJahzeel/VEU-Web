import streamlit as st
from utils.connection import obtener_conteo_por_tipo_y_estado  # 🔵 Importar la función correcta

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
        # Nota: el filtro aún no se aplica, pero ya está preparado

    # Obtener datos de las categorías
    categorias_data = obtener_conteo_por_tipo_y_estado()

    if not categorias_data:
        st.warning("No se encontraron datos de categorías.")
        return

    # 🔵 Ordenar categorías por el total de reportes (resueltos + no resueltos)
    categorias_ordenadas = sorted(
        categorias_data.items(),
        key=lambda x: x[1].get("resueltos", 0) + x[1].get("no_resueltos", 0),
        reverse=True
    )

    # 🔵 Tomar solo las 4 primeras
    categorias_top4 = categorias_ordenadas[:4]

    # Crear columnas para las tarjetas
    cols = st.columns(len(categorias_top4))

    # Mostrar tarjetas de categorías
    for idx, (categoria, datos) in enumerate(categorias_top4):
        with cols[idx]:
            st.markdown(f"""
            <div class='category-card'>
                <div class='icon'>📋</div> <!-- Puedes personalizar el ícono -->
                <h4>{categoria}</h4>
                <div>
                    <span>No resueltos</span>
                    <div class='count-box'>{datos.get('no_resueltos', 0)}</div>
                </div>
                <div>
                    <span>Resueltos</span>
                    <div class='count-box'>{datos.get('resueltos', 0)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
