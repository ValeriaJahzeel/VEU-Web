import streamlit as st
import plotly.graph_objects as go
from utils.data import obtener_datos_barras, obtener_datos_lineas

def mostrar_estadisticas():
    """Muestra la sección de estadísticas con gráficos"""
    # Título de la sección
    st.markdown("<h2 class='reportes-section'>Estadísticas</h2>", unsafe_allow_html=True)
    
    # Gráfica de barras
    mostrar_grafica_barras()
    
    # Gráfica de líneas
    mostrar_grafica_lineas()

def mostrar_grafica_barras():
    """Muestra la gráfica de barras apiladas para reportes por tipo"""
    st.markdown("<h3>Reportes por tipo</h3>", unsafe_allow_html=True)
    
    # Obtener datos para la gráfica
    meses, tipos_reportes, colores, datos_por_tipo = obtener_datos_barras()
    
    # Crear la gráfica de barras apiladas
    fig_barras = go.Figure()
    
    for i, tipo in enumerate(tipos_reportes):
        fig_barras.add_trace(go.Bar(
            x=meses,
            y=datos_por_tipo[tipo],
            name=tipo,
            marker_color=colores[i % len(colores)]
        ))
    
    fig_barras.update_layout(
        barmode='stack',
        title='Reportes mensuales por tipo',
        xaxis_title='Mes',
        yaxis_title='Número de reportes',
        legend_title='Tipo de reporte',
        template='plotly_white',
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    # Mostrar la gráfica de barras apiladas en una tarjeta
    st.markdown("<div class='stats-card'>", unsafe_allow_html=True)
    st.plotly_chart(fig_barras, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def mostrar_grafica_lineas():
    """Muestra la gráfica de líneas temporales"""
    st.markdown("<h3>Línea temporal</h3>", unsafe_allow_html=True)
    
    # Obtener datos para la gráfica
    df_lineas = obtener_datos_lineas()
    
    # Crear la gráfica de líneas
    fig_lineas = go.Figure()
    
    fig_lineas.add_trace(go.Scatter(
        x=df_lineas['fecha'],
        y=df_lineas['Total'],
        mode='lines+markers',
        name='Total',
        line=dict(color='#1f77b4', width=3)
    ))
    
    fig_lineas.add_trace(go.Scatter(
        x=df_lineas['fecha'],
        y=df_lineas['Resueltos'],
        mode='lines+markers',
        name='Resueltos',
        line=dict(color='#2ca02c', width=3)
    ))
    
    fig_lineas.add_trace(go.Scatter(
        x=df_lineas['fecha'],
        y=df_lineas['Pendientes'],
        mode='lines+markers',
        name='Pendientes',
        line=dict(color='#d62728', width=3)
    ))
    
    fig_lineas.update_layout(
        title='Evolución de reportes a lo largo del tiempo',
        xaxis_title='Fecha',
        yaxis_title='Número de reportes',
        legend_title='Estado',
        template='plotly_white',
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    # Mostrar la gráfica de líneas en una tarjeta
    st.markdown("<div class='stats-card'>", unsafe_allow_html=True)
    st.plotly_chart(fig_lineas, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)