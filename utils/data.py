import pandas as pd
import numpy as np
from datetime import datetime

def obtener_datos_categorias():
    """Retorna los datos de ejemplo para las categorías destacadas"""
    categorias_data = {
        "Baches": {"No resueltos": 52, "Resueltos": 10, "icon": "🚧"},
        "Banqueta en mal estado": {"No resueltos": 52, "Resueltos": 10, "icon": "🚶"},
        "Zona poco iluminada": {"No resueltos": 52, "Resueltos": 10, "icon": "💡"},
        "Basura en vía pública": {"No resueltos": 52, "Resueltos": 10, "icon": "🗑️"}
    }
    return categorias_data

def obtener_datos_barras():
    """Retorna los datos para el gráfico de barras apiladas"""
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    tipos_reportes = ['Baches', 'Basura', 'Iluminación', 'Banquetas', 'Otros']
    colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # Crear datos aleatorios para cada tipo de reporte
    datos_por_tipo = {}
    np.random.seed(42)  # Para reproducibilidad de los datos
    
    for tipo in tipos_reportes:
        base = np.random.randint(50, 100)
        datos_por_tipo[tipo] = [base + np.random.randint(-20, 30) for _ in range(len(meses))]
    
    return meses, tipos_reportes, colores, datos_por_tipo

def obtener_datos_lineas():
    """Retorna los datos para el gráfico de líneas temporales"""
    fechas = pd.date_range(end=datetime.now(), periods=12, freq='M')
    series_data = {
        'Total': [150, 120, 180, 200, 170, 220, 280, 230, 190, 250, 270, 220],
        'Resueltos': [100, 80, 120, 140, 110, 140, 210, 150, 120, 170, 180, 140],
        'Pendientes': [50, 40, 60, 60, 60, 80, 70, 80, 70, 80, 90, 80]
    }
    
    df_lineas = pd.DataFrame({
        'fecha': fechas,
        'Total': series_data['Total'],
        'Resueltos': series_data['Resueltos'],
        'Pendientes': series_data['Pendientes']
    })
    
    return df_lineas