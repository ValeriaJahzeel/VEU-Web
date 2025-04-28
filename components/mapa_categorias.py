import streamlit as st
import json

def mostrar_panel_categorias():
    if 'filtros_seleccionados' not in st.session_state:
        st.session_state.filtros_seleccionados = {}

    
    st.markdown("### Categorías", unsafe_allow_html=True)

    with open('categorias.json', 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

        for categoria in datos["categorias"]:
            st.markdown(f"#### {categoria['nombre_categoria']}", unsafe_allow_html=True)

            for area in categoria["areas"]:
                expanded = (categoria['id_categoria'] == 1 and area['id_area'] == 1)

                with st.container():
                    with st.expander(area['nombre_area'], expanded=expanded):
                        for tipo in area["tipos"]:
                            tipo_id = f"tipo_{tipo['id_tipo']}"
                            valor_previo = st.session_state.filtros_seleccionados.get(tipo_id, False)
                            checkbox_seleccionado = st.checkbox(
                                tipo['nombre_tipo'], 
                                value=valor_previo, 
                                key=tipo_id
                            )
                            st.session_state.filtros_seleccionados[tipo_id] = checkbox_seleccionado

    # Filtrar solo los tipos seleccionados
    tipos_seleccionados = [tipo_id for tipo_id, seleccionado in st.session_state.filtros_seleccionados.items() if seleccionado]

    # Si no se seleccionó nada, devolver None
    if not tipos_seleccionados:
        return None
    else:
        return tipos_seleccionados