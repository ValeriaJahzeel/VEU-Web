from connection import connection

def obtener_reportes():
    try:
        supabase = connection() # Obtener la conexión de Supabase
        
        # obtener datos de reportes
        response = supabase.table("reporte").select("fecha_creacion,fecha_resuelto,fk_reporte_tipo,latitud,longitud,codigo_postal").execute()
        
        print("Respuesta completa:", response)
        
        if response and hasattr(response, "data") and response.data:
            data = response.data
            print("Datos obtenidos:")
            for row in data:
                print(row)
            return data
        else:
            print("No se encontraron datos o formato de respuesta inesperado.")
            return []
            
    except Exception as e:
        print(f"Error al obtener reportes: {e}")
        return []


obtener_reportes()