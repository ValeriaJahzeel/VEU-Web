from supabase import create_client
import os
from dotenv import load_dotenv

def get_connection():
    """
    Establece la conexión con Supabase.
    
    Returns:
        Objeto de conexión a Supabase
    """
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    # Verificar que se hayan cargado las variables de entorno
    if not supabase_url or not supabase_key:
        raise ValueError("No se encontraron las variables de entorno SUPABASE_URL o SUPABASE_KEY")
    
    # Crear y devolver la conexión
    supabase = create_client(supabase_url, supabase_key)
    return supabase

# Función para obtener datos de reportes de Supabase
def obtener_reportes():
    """
    Consulta la tabla 'reporte' en Supabase para obtener los datos.
    
    Returns:
        Lista de diccionarios con los datos de los reportes
    """
    try:
        # Obtener la conexión de Supabase
        supabase = get_connection()
        
        # Realizar la consulta
        response = supabase.table("reporte").select("fecha_creacion,fecha_resuelto,fk_reporte_tipo,latitud,longitud,codigo_postal").execute()
        
        # Procesar y devolver los datos
        if response and hasattr(response, "data") and response.data:
            return response.data
        else:
            print("No se encontraron datos o formato de respuesta inesperado.")
            return []
            
    except Exception as e:
        print(f"Error al obtener reportes: {e}")
        return []

# Función para obtener datos agrupados por tipo de reporte
def obtener_reportes_por_tipo():
    """
    Consulta y agrupa los reportes por tipo.
    
    Returns:
        Diccionario con los datos agrupados por tipo de reporte
    """
    try:
        # Esta es una implementación de ejemplo. En una implementación real,
        # se haría una consulta más específica a Supabase para obtener datos agrupados.
        
        reportes = obtener_reportes()
        
        # Agrupar por tipo
        reportes_por_tipo = {}
        for reporte in reportes:
            tipo = reporte.get("fk_reporte_tipo", "Otro")
            if tipo not in reportes_por_tipo:
                reportes_por_tipo[tipo] = []
            reportes_por_tipo[tipo].append(reporte)
        
        return reportes_por_tipo
    
    except Exception as e:
        print(f"Error al agrupar reportes por tipo: {e}")
        return {}

# Función para obtener conteo de reportes resueltos y no resueltos
def obtener_conteo_por_estado():
    """
    Cuenta los reportes por estado (resuelto/no resuelto).
    
    Returns:
        Diccionario con conteo de reportes por estado
    """
    try:
        reportes = obtener_reportes()
        
        resueltos = 0
        no_resueltos = 0
        
        for reporte in reportes:
            if reporte.get("fecha_resuelto"):
                resueltos += 1
            else:
                no_resueltos += 1
        
        return {
            "resueltos": resueltos,
            "no_resueltos": no_resueltos
        }
    
    except Exception as e:
        print(f"Error al contar reportes por estado: {e}")
        return {"resueltos": 0, "no_resueltos": 0}

# Si quieres probar la conexión directamente al ejecutar este archivo
if __name__ == "__main__":
    try:
        connection = get_connection()
        print("Conexión a Supabase establecida correctamente")
        
        reportes = obtener_reportes()
        print(f"Se obtuvieron {len(reportes)} reportes")
    except Exception as e:
        print(f"Error al conectar con Supabase: {e}")