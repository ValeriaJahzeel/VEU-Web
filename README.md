# VEU - "La flota que observa la ciudad"

![Banner del Proyecto](\img\logoVEU.jpeg)

## Descripción

Este proyecto fue desarrollado en base a las problemáticas presentadas por VEU en el Mobility Hackaton 2025. Esta problemática se resolvió mediante el diseño y la programacion de un dashboard interactivo desarrollado con Streamlit para visualizar y analizar reportes georeferenciados de incidentes en las carreteras. Permite filtrar por código postal, ver estadísticas temporales y explorar categorías destacadas de reportes.

## Características

- **Visualización geográfica**: Mapa interactivo con marcadores para ubicar reportes.
- **Filtrado por código postal**: Búsqueda de reportes por CP con visualización de tarjetas informativas.
- **Categorías destacadas**: Visualización de las principales categorías de reportes.
- **Estadísticas mensuales**: Gráficos temporales y distribución de reportes por tipo.
- **Panel de categorías**: Filtrado por tipo de reporte mediante un panel de categorías jerárquico.
- **Herramientas de diagnóstico**: Funcionalidades integradas para depuración de datos.

## Tecnologías utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-77B829?style=for-the-badge&logo=folium&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)


## Interfaces 
![Primera interfaz](\img\interfaz1.jpeg)
![Segunda interfaz](\img\interfaz2.jpeg)

![Funcionalidad](\img\funcionalidad.gif)

## Guía de Uso

### Filtrado por Código Postal
1. Ingresa un código postal en el campo de texto en la sección "Filtrar por CP"
2. Haz clic en "Buscar"
3. Verás la información del código postal y los reportes asociados
4. El mapa se centrará automáticamente en la ubicación del código postal

### Selección de Categorías
1. Navega por las categorías en el panel izquierdo
2. Selecciona las categorías que deseas visualizar marcando las casillas
3. El mapa y las estadísticas se actualizarán según la selección

### Visualización de Estadísticas
1. Selecciona el año y mes que deseas analizar
2. Haz clic en "Aplicar"
3. Explora los gráficos de línea, barras y pie que muestran la distribución de reportes


## Detalles Técnicos

### Conexión con Supabase
El dashboard se conecta a una base de datos Supabase que contiene los reportes con su información geográfica, tipo de reporte, fechas y estado de resolución.

```python
# Ejemplo de conexión
from supabase import create_client
import os
from dotenv import load_dotenv

def get_connection():
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    supabase = create_client(supabase_url, supabase_key)
    return supabase
```

### Estructura de Datos
Los reportes contienen la siguiente información:
- ID de reporte
- Fecha de creación
- Fecha de resolución (si está resuelto)
- Tipo de reporte (referencia a tabla de tipos)
- Latitud y longitud
- Código postal
- Número de eventos

### Visualización de Mapas
Utilizamos Folium para crear mapas interactivos que muestran los reportes geograficamente:

```python
# Ejemplo de creación de mapa
import folium
from streamlit_folium import folium_static

m = folium.Map(location=[latitud, longitud], zoom_start=15)
folium.Marker([lat, lon], popup=popup_text).add_to(m)
folium_static(m, width=600)
```

## Equipo

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/MikeszIPN">
        <img src="https://avatars.githubusercontent.com/u/125789083?v=4" width="100px;" alt="Desarrollador 1"/>
        <br />
        <sub><b>Miguel Angel Sánchez Zanjuanpa</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/NavilP">
        <img src="https://avatars.githubusercontent.com/u/125292694?v=4" width="100px;" alt="Desarrollador 2"/>
        <br />
        <sub><b>Navil Pineda Rugerio</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Senorita-glez">
        <img src="https://avatars.githubusercontent.com/u/77082096?v=4" width="100px;" alt="Desarrollador 3"/>
        <br />
        <sub><b>Daphne Sophia Gonzalez Cano</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/ValeriaJahzeel">
        <img src="https://avatars.githubusercontent.com/u/49892759?v=4" width="100px;" alt="Desarrollador 3"/>
        <br />
        <sub><b>Valeria Jahzeel Castañón Hernández</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/DiegoCastr00">
        <img src="https://avatars.githubusercontent.com/u/124998012?v=4" width="100px;" alt="Desarrollador 3"/>
        <br />
        <sub><b>Diego Castro Elvira</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Betucciny">
        <img src="https://avatars.githubusercontent.com/u/86085514?v=4" width="100px;" alt="Desarrollador 3"/>
        <br />
        <sub><b>Roberto Ángel Herrera</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Nancy-07">
        <img src="https://avatars.githubusercontent.com/u/125350005?v=4" width="100px;" alt="Desarrollador 3"/>
        <br />
        <sub><b>Nancy Galicia Cocoletzi</b></sub>
      </a>
    </td>
  </tr>
</table>

