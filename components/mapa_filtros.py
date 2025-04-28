import streamlit as st
import json
import pandas as pd
import folium
from streamlit_folium import folium_static
from utils.connection import obtener_reportes

def mostrar_filtro_cp():
    """Muestra el panel de filtro por código postal y los resultados filtrados en tarjetas"""
    st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
    st.markdown("<h3>Filtrar por CP</h3>", unsafe_allow_html=True)
    
    # Input para el código postal
    codigo_postal = st.text_input("Ingresa el código postal", key="input_cp")
    
    # Retornar el código postal ingresado para usarlo en la actualización del mapa
    return codigo_postal

def obtener_reportes_por_cp(codigo_postal):
    """
    Filtra los reportes por código postal
    
    Args:
        codigo_postal: Código postal a filtrar
        
    Returns:
        Lista de reportes filtrados
    """
    if not codigo_postal:
        return []
    
    # Obtener todos los reportes
    reportes = obtener_reportes()
    
    # Filtrar por código postal (asegurarse de que ambos sean strings para comparar)
    cp_str = str(codigo_postal).strip()
    filtrados = []
    
    for reporte in reportes:
        if reporte.get("codigo_postal") is not None:
            reporte_cp = str(reporte.get("codigo_postal")).strip()
            if reporte_cp == cp_str:
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
        
        # Si hay reportes, centrar el mapa en el primer reporte
        if reportes_filtrados:
            try:
                # Tomar las coordenadas del primer reporte para centrar el mapa
                latitud = reportes_filtrados[0].get("latitud", 19.4326)
                longitud = reportes_filtrados[0].get("longitud", -99.1332)
                
                # Crear el mapa centrado en la ubicación del primer reporte
                m = folium.Map(location=[latitud, longitud], zoom_start=15)
                
                # Agregar marcadores para todos los reportes filtrados
                for reporte in reportes_filtrados:
                    lat = reporte.get("latitud")
                    lon = reporte.get("longitud")
                    tipo = reporte.get("fk_reporte_tipo", "Sin tipo")
                    fecha = reporte.get("fecha_creacion", "Sin fecha")
                    
                    # Solo agregar marcador si tiene coordenadas válidas
                    if lat and lon:
                        popup_text = f"Tipo: {tipo}<br>Fecha: {fecha}"
                        folium.Marker([lat, lon], popup=popup_text).add_to(m)
                
                # Mostrar el mapa con los reportes filtrados
                return m
            except Exception as e:
                st.error(f"Error al mostrar el mapa filtrado: {str(e)}")
                # En caso de error, mostrar mapa predeterminado
                m = folium.Map(location=[19.4326, -99.1332], zoom_start=13)
                return m
        else:
            # Si no hay reportes para ese CP, mostrar mapa sin marcadores
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

def mostrar_info_cp_cards(codigo_postal):
    """
    Muestra la información de un código postal específico en tarjetas solo si 
    el código postal existe en la base de datos de Supabase.
    
    Args:
        codigo_postal: Código postal para mostrar información
    """
    if not codigo_postal:
        return
    
    # Verificar si hay reportes en Supabase para este código postal
    reportes_filtrados = obtener_reportes_por_cp(codigo_postal)
    
    # Si no hay reportes, mostrar mensaje y salir
    if not reportes_filtrados:
        st.warning(f"No hay reportes registrados para el código postal {codigo_postal}")
        return
    
    try:
        # Agregar CSS para las tarjetas
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
        
        # Intentar cargar el archivo JSON para obtener información adicional del CP
        try:
            with open('./CP/output.json', 'r', encoding="utf-8") as f:
                data = json.load(f)
            
            # Filtrar por código postal
            filtrados = []
            for item in data:
                if isinstance(item, dict) and 'd_codigo' in item:
                    if str(item['d_codigo']) == codigo_postal:
                        filtrados.append(item)
            
            # Mostrar resultados si hay coincidencias en el JSON
            if filtrados:
                st.markdown("<h4>Información del código postal:</h4>", unsafe_allow_html=True)
                
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
                # Si no hay info del CP en el JSON pero sí hay reportes en Supabase
                st.markdown(f"""
                <div class="cp-card">
                    <div class="codigo-postal">CP: {codigo_postal}</div>
                    <div class="reportes-count">Reportes encontrados: {len(reportes_filtrados)}</div>
                </div>
                """, unsafe_allow_html=True)
                
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Si no podemos acceder al JSON pero tenemos reportes
            st.markdown(f"""
            <div class="cp-card">
                <div class="codigo-postal">CP: {codigo_postal}</div>
                <div class="reportes-count">Reportes encontrados: {len(reportes_filtrados)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Mostrar tabla de reportes
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

def mostrar_mapa_y_filtros():
    """Muestra la sección del mapa y los filtros laterales"""
    from components.mapa_categorias import mostrar_panel_categorias
    
    # Crear checkbox debug (opcional)
    st.sidebar.checkbox("Activar modo debug", value=False, key="debug_mode")
    
    # Crear 3 columnas para la sección
    col1, col2, col3 = st.columns([1, 2, 1])

    # Columna 1: Categorías
    with col1:
        tipos_seleccionados = mostrar_panel_categorias()
        # El valor de tipos_seleccionados puede usarse para filtrar en el futuro

    # Columna 3: Filtro por CP
    with col3:
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        codigo_postal = mostrar_filtro_cp()
        mostrar_info_cp_cards(codigo_postal)
        st.markdown("</div>", unsafe_allow_html=True)

    # Columna 2: Mapa
    with col2:
        mapa = mostrar_mapa_filtrado(codigo_postal)
        folium_static(mapa, width=600)