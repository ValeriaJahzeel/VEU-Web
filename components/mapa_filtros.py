import streamlit as st
import json
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

def mostrar_filtro_cp():
    """Muestra el panel de filtro por código postal y los resultados filtrados en tarjetas"""
    st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
    st.markdown("<h3>Filtrar por CP</h3>", unsafe_allow_html=True)
    
    # Input para el código postal
    codigo_postal = st.text_input("Ingresa el código postal", key="input_cp")
    
    # Botón para buscar el código postal
    buscar = st.button("Buscar", use_container_width=True)
    
    # Inicializar la session_state si no existe
    if "filtro_cp" not in st.session_state:
        st.session_state.filtro_cp = ""
    
    # Guardar el CP en session_state si se pulsa el botón o si se presiona Enter
    if buscar and codigo_postal:
        # Limpiar el código postal (quitar espacios y asegurar formato)
        codigo_postal_limpio = codigo_postal.strip()
        st.session_state.filtro_cp = codigo_postal_limpio
    
    # Añadimos un botón para limpiar el filtro
    if st.session_state.get("filtro_cp"):
        if st.button("Limpiar filtro", use_container_width=True):
            st.session_state.filtro_cp = ""
            # Forzar recarga de la página para limpiar resultados
            st.experimental_rerun()
    
    # Devolver el código postal guardado en session_state
    return st.session_state.get("filtro_cp", "")

def obtener_reportes_por_cp(codigo_postal):
    """
    Filtra los reportes por código postal
    
    Args:
        codigo_postal: Código postal a filtrar
        
    Returns:
        Lista de reportes filtrados
    """
    from utils.connection import obtener_reportes
    
    if not codigo_postal:
        return []
    
    # Obtener todos los reportes
    reportes = obtener_reportes()
    
    # Implementar múltiples estrategias de comparación para manejar diferentes formatos de código postal
    filtrados = []
    for reporte in reportes:
        cp_reporte = reporte.get("codigo_postal")
        
        # Cuando el CP es None o vacío, continuar con el siguiente reporte
        if cp_reporte is None or cp_reporte == "":
            continue
            
        # Convertir ambos CPs a string para comparación
        cp_reporte_str = str(cp_reporte).strip()
        codigo_postal_str = str(codigo_postal).strip()
        
        # Intentar coincidencia exacta y coincidencia sin ceros iniciales
        if (cp_reporte_str == codigo_postal_str or 
            cp_reporte_str.lstrip('0') == codigo_postal_str.lstrip('0')):
            filtrados.append(reporte)
    
    return filtrados

def mostrar_mapa_filtrado(codigo_postal=None):
    """
    Muestra el mapa con reportes filtrados por código postal
    
    Args:
        codigo_postal: Código postal para filtrar los reportes
    """
    # Si hay un código postal, obtener reportes filtrados
    if codigo_postal:
        reportes_filtrados = obtener_reportes_por_cp(codigo_postal)
        
        # Si no hay reportes, mostrar mapa predeterminado con aviso
        if not reportes_filtrados:
            m = folium.Map(location=[19.4326, -99.1332], zoom_start=13)
            folium.Marker(
                [19.4326, -99.1332],
                popup=f"<b>No se encontraron reportes para el CP: {codigo_postal}</b>",
                icon=folium.Icon(color='red', icon='exclamation', prefix='fa')
            ).add_to(m)
            return m
            
        # Si hay reportes, tratar de obtener coordenadas
        coordenadas_cp = obtener_coordenadas_cp(codigo_postal)
        
        try:
            # Definir ubicación central para el mapa
            if coordenadas_cp:
                # Si tenemos coordenadas del CP, usarlas
                latitud, longitud = coordenadas_cp
            elif reportes_filtrados:
                # O usar el primer reporte disponible
                latitud = reportes_filtrados[0].get("latitud", 19.4326)
                longitud = reportes_filtrados[0].get("longitud", -99.1332)
            else:
                # Fallback a Ciudad de México
                latitud, longitud = 19.4326, -99.1332
            
            # Crear el mapa centrado en la ubicación encontrada
            m = folium.Map(location=[latitud, longitud], zoom_start=15)
            
            # Agregar marcador para el CP con un ícono especial
            if coordenadas_cp:
                folium.Marker(
                    [coordenadas_cp[0], coordenadas_cp[1]],
                    popup=f"<b>Código Postal: {codigo_postal}</b>",
                    icon=folium.Icon(color='red', icon='home', prefix='fa')
                ).add_to(m)
            
            # Crear un cluster para los reportes
            marker_cluster = MarkerCluster().add_to(m)
            
            # Agregar marcadores para todos los reportes filtrados
            for reporte in reportes_filtrados:
                lat = reporte.get("latitud")
                lon = reporte.get("longitud")
                tipo = reporte.get("fk_reporte_tipo", "Sin tipo")
                fecha = reporte.get("fecha_creacion", "Sin fecha")
                
                # Solo agregar marcador si tiene coordenadas válidas
                if lat and lon:
                    # Crear un popup más informativo
                    popup_text = f"""
                    <div style="width: 200px">
                        <h4>Reporte</h4>
                        <b>Tipo:</b> {tipo}<br>
                        <b>Fecha:</b> {fecha}<br>
                        <b>Estado:</b> {"Resuelto" if reporte.get("fecha_resuelto") else "Pendiente"}
                    </div>
                    """
                    folium.Marker(
                        [lat, lon], 
                        popup=folium.Popup(popup_text, max_width=300)
                    ).add_to(marker_cluster)
            
            return m
        except Exception as e:
            st.error(f"Error al mostrar el mapa filtrado: {str(e)}")
            # En caso de error, mostrar mapa predeterminado
            m = folium.Map(location=[19.4326, -99.1332], zoom_start=13)
            return m
    else:
        # Si no hay código postal, mostrar mapa predeterminado con algunos ejemplos
        m = folium.Map(location=[19.4326, -99.1332], zoom_start=13)
        
        # Agregar algunos marcadores de ejemplo
        folium.Marker([19.4326, -99.1332], popup="Reporte 1: Bache").add_to(m)
        folium.Marker([19.4396, -99.1400], popup="Reporte 2: Iluminación").add_to(m)
        folium.Marker([19.4250, -99.1250], popup="Reporte 3: Basura").add_to(m)
        
        return m

def obtener_coordenadas_cp(codigo_postal):
    """
    Intenta obtener las coordenadas geográficas aproximadas para un código postal
    
    Args:
        codigo_postal: Código postal a buscar
        
    Returns:
        Tupla con (latitud, longitud) o None si no se encuentra
    """
    try:
        # Intentar cargar el archivo JSON de códigos postales
        with open('./CP/output.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
        
        # Buscar el código postal
        for item in data:
            if isinstance(item, dict) and 'd_codigo' in item:
                if str(item['d_codigo']) == codigo_postal:
                    # Si el registro tiene coordenadas explícitas, usarlas
                    if 'latitud' in item and 'longitud' in item:
                        return float(item['latitud']), float(item['longitud'])
                    
                    # Si no tiene coordenadas explícitas pero sí CP, buscar reportes con ese CP
                    reportes = obtener_reportes_por_cp(codigo_postal)
                    if reportes:
                        for reporte in reportes:
                            if reporte.get('latitud') and reporte.get('longitud'):
                                return float(reporte['latitud']), float(reporte['longitud'])
        
        # Si no encontramos coordenadas, retornar None
        return None
    
    except Exception as e:
        st.error(f"Error al obtener coordenadas para CP: {str(e)}")
        return None

def mostrar_info_cp_cards(codigo_postal):
    if not codigo_postal:
        return
    
    try:
        # Primero verificar si hay reportes para este CP
        reportes_filtrados = obtener_reportes_por_cp(codigo_postal)
        
        # Si no hay reportes, mostrar mensaje claro y no continuar
        if not reportes_filtrados:
            st.error(f"No se encontraron reportes para el código postal {codigo_postal}.")
            
            # Intentar mostrar al menos información del CP si está disponible
            try:
                with open('./CP/output.json', 'r', encoding="utf-8") as f:
                    data = json.load(f)
                
                # Buscar información del CP aunque no haya reportes
                cp_info = None
                for item in data:
                    if isinstance(item, dict) and 'd_codigo' in item:
                        if str(item['d_codigo']).strip() == str(codigo_postal).strip():
                            cp_info = item
                            break
                
                if cp_info:
                    # Mostrar al menos la información del CP
                    st.info("Se encontró información sobre este código postal, pero no hay reportes registrados.")
                    
                    # Obtener valores con fallback
                    estado = cp_info.get('d_estado', 'N/A')
                    codigo = cp_info.get('d_codigo', 'N/A')
                    asenta = cp_info.get('d_asenta', 'N/A')
                    municipio = cp_info.get('d_mnpio', cp_info.get('D_mnpio', 'N/A'))
                    
                    # Mostrar la información
                    st.markdown(f"""
                    <style>
                        .cp-info-card {{
                            background-color: #f0f2f6;
                            border-radius: 5px;
                            padding: 10px;
                            margin-top: 10px;
                        }}
                    </style>
                    <div class="cp-info-card">
                        <p><b>Estado:</b> {estado}</p>
                        <p><b>Municipio:</b> {municipio}</p>
                        <p><b>Colonia:</b> {asenta}</p>
                    </div>
                    """, unsafe_allow_html=True)
            except:
                pass
                
            return
        
        # Continuar con el resto del código solo si hay reportes
        # Agregar CSS para las tarjetas (solo si hay reportes)
        st.markdown("""
        <style>
            .cp-card {
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
                padding: 15px;
                margin-bottom: 15px;
                border-left: 5px solid #1A4E8C;
            }
            .estado-nombre {
                font-size: 1.5rem;
                font-weight: bold;
                color: #1A4E8C;
                margin-bottom: 5px;
            }
            .codigo-postal {
                font-size: 1.2rem;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            .card-detail {
                margin-bottom: 5px;
                color: #555;
            }
            .reportes-count {
                background-color: #1A4E8C;
                color: white;
                padding: 5px 10px;
                border-radius: 15px;
                font-weight: bold;
                display: inline-block;
                margin-top: 10px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Intentar cargar el archivo JSON para información adicional del CP
        try:
            with open('./CP/output.json', 'r', encoding="utf-8") as f:
                data = json.load(f)
            
            # Filtrar por código postal
            filtrados = []
            for item in data:
                if isinstance(item, dict) and 'd_codigo' in item:
                    if str(item['d_codigo']).strip() == str(codigo_postal).strip():
                        filtrados.append(item)
                        
            # Mostrar información del CP si está disponible
            if filtrados:
                st.markdown("<h4>Información del código postal:</h4>", unsafe_allow_html=True)
                st.success(f"Se encontraron {len(reportes_filtrados)} reportes para este código postal")
                
                # Mostrar cada resultado como una tarjeta
                for item in filtrados:
                    # Obtener valores con fallback en caso de que no existan
                    estado = item.get('d_estado', 'N/A')
                    codigo = item.get('d_codigo', 'N/A')
                    asenta = item.get('d_asenta', 'N/A')
                    
                    # Manejar ambas variantes de municipio
                    municipio = item.get('d_mnpio', item.get('D_mnpio', 'N/A'))
                    
                    # Renderizar la tarjeta con HTML
                    st.markdown(f"""
                    <div class="cp-card">
                        <div class="estado-nombre">{estado}</div>
                        <div class="codigo-postal">CP: {codigo}</div>
                        <div class="card-detail"><b>Colonia:</b> {asenta}</div>
                        <div class="card-detail"><b>Municipio:</b> {municipio}</div>
                        <div class="reportes-count">Reportes encontrados: {len(reportes_filtrados)}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Si no hay info del CP pero sí hay reportes, mostrar tarjeta genérica
                st.markdown("<h4>Información del código postal:</h4>", unsafe_allow_html=True)
                st.success(f"Se encontraron {len(reportes_filtrados)} reportes para este código postal")
                st.markdown(f"""
                <div class="cp-card">
                    <div class="codigo-postal">CP: {codigo_postal}</div>
                    <div class="card-detail"><b>Nota:</b> No se encontró información adicional para este código postal</div>
                    <div class="reportes-count">Reportes encontrados: {len(reportes_filtrados)}</div>
                </div>
                """, unsafe_allow_html=True)
        
        except (FileNotFoundError, json.JSONDecodeError):
            # Si hay un problema con el archivo de CP pero hay reportes, mostrar info básica
            st.markdown("<h4>Información del código postal:</h4>", unsafe_allow_html=True)
            st.success(f"Se encontraron {len(reportes_filtrados)} reportes para este código postal")
            st.markdown(f"""
            <div class="cp-card">
                <div class="codigo-postal">CP: {codigo_postal}</div>
                <div class="card-detail"><b>Nota:</b> No se pudo cargar información adicional del código postal</div>
                <div class="reportes-count">Reportes encontrados: {len(reportes_filtrados)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Mostrar los reportes encontrados (esto ocurre siempre que hay reportes)
        st.markdown("<h4>Reportes encontrados:</h4>", unsafe_allow_html=True)
        
        # Convertir a DataFrame para mejor visualización
        df = pd.DataFrame(reportes_filtrados)
        
        # Mostrar una versión simplificada del DataFrame
        cols_to_show = ['fecha_creacion', 'fecha_resuelto', 'fk_reporte_tipo', 'latitud', 'longitud']
        cols_display = {
            'fecha_creacion': 'Fecha de creación',
            'fecha_resuelto': 'Fecha de resolución',
            'fk_reporte_tipo': 'Tipo de reporte',
            'latitud': 'Latitud',
            'longitud': 'Longitud'
        }
        
        # Seleccionar columnas que existen en el DataFrame
        available_cols = [col for col in cols_to_show if col in df.columns]
        
        if available_cols:
            df_display = df[available_cols]
            # Renombrar columnas para mejor presentación
            df_display = df_display.rename(columns={k: v for k, v in cols_display.items() if k in available_cols})
            st.dataframe(df_display, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
        import traceback
        st.error(traceback.format_exc())

def mostrar_mapa_y_filtros():
    """Muestra la sección del mapa y los filtros laterales"""
    from components.mapa_categorias import mostrar_panel_categorias
    
    # Crear una fila inicial para un mensaje de depuración (opcional)
    if st.checkbox("Mostrar información de depuración", value=False):
        with st.expander("Datos de depuración"):
            st.write("Estado de la sesión:", st.session_state)
            
            # Probar la conexión a la base de datos
            from utils.connection import obtener_reportes
            reportes = obtener_reportes()
            st.write(f"Total de reportes en la base de datos: {len(reportes)}")
            
            # Mostrar ejemplos de formatos de CP
            if reportes:
                st.write("Ejemplos de códigos postales en la base de datos:")
                cp_ejemplos = [reporte.get("codigo_postal") for reporte in reportes[:5] if "codigo_postal" in reporte]
                for i, cp in enumerate(cp_ejemplos):
                    st.write(f"CP {i+1}: '{cp}' (tipo: {type(cp).__name__})")
    
    # Crear 3 columnas para la sección
    col1, col2, col3 = st.columns([1, 2, 1])

    # Columna 1: Categorías
    with col1:
        mostrar_panel_categorias()

    # Columna 3: Filtro por CP (antes que el mapa para obtener el código postal)
    with col3:
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        codigo_postal = mostrar_filtro_cp()
        mostrar_info_cp_cards(codigo_postal)
        st.markdown("</div>", unsafe_allow_html=True)

    # Columna 2: Mapa (ahora usando el código postal)
    with col2:
        mapa = mostrar_mapa_filtrado(codigo_postal)
        folium_static(mapa, width=600)