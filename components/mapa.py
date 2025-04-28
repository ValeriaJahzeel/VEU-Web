import folium
from streamlit_folium import folium_static

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