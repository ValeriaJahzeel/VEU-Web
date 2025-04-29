# Dashboard de Reportes

![Banner del Proyecto](https://via.placeholder.com/800x200/1A4E8C/FFFFFF?text=Dashboard+de+Reportes)

## 📋 Descripción

Este proyecto es un dashboard interactivo desarrollado con Streamlit para visualizar y analizar reportes georeferenciados. Permite filtrar por código postal, ver estadísticas temporales y explorar categorías destacadas de reportes.

## ✨ Características

- **Visualización geográfica**: Mapa interactivo con marcadores para ubicar reportes.
- **Filtrado por código postal**: Búsqueda de reportes por CP con visualización de tarjetas informativas.
- **Categorías destacadas**: Visualización de las principales categorías de reportes.
- **Estadísticas mensuales**: Gráficos temporales y distribución de reportes por tipo.
- **Panel de categorías**: Filtrado por tipo de reporte mediante un panel de categorías jerárquico.
- **Herramientas de diagnóstico**: Funcionalidades integradas para depuración de datos.

## 🔧 Tecnologías utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-77B829?style=for-the-badge&logo=folium&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)

## 📁 Estructura del proyecto

```
dashboard/
├── principal.py                  # Punto de entrada principal
├── requirements.txt              # Dependencias del proyecto
├── .env                          # Variables de entorno (no incluidas en repositorio)
├── categorias.json               # Estructura de categorías para el panel de filtro
├── components/                   # Componentes modulares del dashboard
│   ├── categorias_destacadas.py  # Componente de tarjetas de categorías destacadas
│   ├── estadisticas.py           # Visualizaciones estadísticas por mes
│   ├── header.py                 # Cabecera del dashboard
│   ├── mapa.py                   # Mapa básico (versión simple)
│   ├── mapa_categorias.py        # Panel de filtrado por categorías
│   └── mapa_filtros.py           # Mapa con filtros por CP y visualización de datos
├── CP/                           # Datos de códigos postales
│   └── output.json               # Base de datos de códigos postales
├── csv_ejemplos/                 # Archivos CSV auxiliares
│   └── tipo_rows.csv             # Datos de tipos de reporte
├── scripts/                      # Scripts auxiliares
│   ├── visualizar_datos.py       # Explorador de datos de la BD
│   └── analizar_codigos_postales.py  # Análisis específico de códigos postales
└── utils/                        # Utilidades compartidas
    ├── connection.py             # Conexión a Supabase y funciones de datos
    └── styles.py                 # Estilos CSS para el dashboard
```

## 🚀 Instalación y ejecución

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. Clonar este repositorio:
```bash
git clone https://github.com/tu-usuario/dashboard-reportes.git
cd dashboard-reportes
```

2. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

3. Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Ejecución

Para ejecutar el dashboard principal:
```bash
streamlit run principal.py
```

Para herramientas adicionales:
```bash
# Visualizador de datos
streamlit run scripts/visualizar_datos.py

# Analizador de códigos postales
streamlit run scripts/analizar_codigos_postales.py
```

## 📊 Interfaces del Dashboard

### Pantalla Principal
La pantalla principal del dashboard integra todos los componentes y permite una visualización completa de los datos.

![Dashboard Principal](https://via.placeholder.com/800x400/1A4E8C/FFFFFF?text=Dashboard+Principal)

### Categorías Destacadas
Tarjetas que muestran las principales categorías de reportes con conteo de resueltos y no resueltos.

![Categorías Destacadas](https://via.placeholder.com/800x200/3E6FB9/FFFFFF?text=Categorías+Destacadas)

### Mapa con Filtros
Mapa interactivo que permite visualizar los reportes geográficamente y filtrar por código postal.

![Mapa con Filtros](https://via.placeholder.com/800x400/1A4E8C/FFFFFF?text=Mapa+con+Filtros)

### Información de Código Postal
Tarjetas informativas que muestran datos del código postal y los reportes asociados.

![Información de Código Postal](https://via.placeholder.com/800x300/3E6FB9/FFFFFF?text=Tarjetas+de+Código+Postal)

### Estadísticas Mensuales
Gráficos y análisis estadísticos de los reportes por mes, incluyendo distribución por tipo y evolución temporal.

![Estadísticas Mensuales](https://via.placeholder.com/800x400/1A4E8C/FFFFFF?text=Estadísticas+Mensuales)

### Herramientas de Diagnóstico
Visualizador de datos y analizador de códigos postales para diagnóstico y exploración profunda.

![Herramientas de Diagnóstico](https://via.placeholder.com/800x300/3E6FB9/FFFFFF?text=Herramientas+de+Diagnóstico)

## 📝 Guía de Uso

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

### Herramientas de Diagnóstico
1. Para un análisis más profundo, ejecuta los scripts auxiliares
2. Visualiza datos específicos de la base de datos
3. Analiza la distribución de códigos postales y reportes

## 🔍 Detalles Técnicos

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

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Haz un fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Equipo

### Desarrolladores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/desarrollador1">
        <img src="https://via.placeholder.com/100x100/1A4E8C/FFFFFF?text=Dev1" width="100px;" alt="Desarrollador 1"/>
        <br />
        <sub><b>Nombre Desarrollador 1</b></sub>
      </a>
      <br />
      <a href="https://linkedin.com/in/desarrollador1" title="LinkedIn">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white" />
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/desarrollador2">
        <img src="https://via.placeholder.com/100x100/3E6FB9/FFFFFF?text=Dev2" width="100px;" alt="Desarrollador 2"/>
        <br />
        <sub><b>Nombre Desarrollador 2</b></sub>
      </a>
      <br />
      <a href="https://linkedin.com/in/desarrollador2" title="LinkedIn">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white" />
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/desarrollador3">
        <img src="https://via.placeholder.com/100x100/2C5AA0/FFFFFF?text=Dev3" width="100px;" alt="Desarrollador 3"/>
        <br />
        <sub><b>Nombre Desarrollador 3</b></sub>
      </a>
      <br />
      <a href="https://linkedin.com/in/desarrollador3" title="LinkedIn">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white" />
      </a>
    </td>
  </tr>
</table>

## 📞 Contacto

Para cualquier consulta o sugerencia, no dudes en contactarnos:

- Correo electrónico: [tu-correo@ejemplo.com](mailto:tu-correo@ejemplo.com)
- GitHub: [tu-usuario](https://github.com/tu-usuario)

---

Desarrollado con ❤️ por [Tu Nombre/Organización]