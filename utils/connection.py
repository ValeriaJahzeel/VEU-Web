from supabase import create_client
import os
from dotenv import load_dotenv

def get_connection():
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

# ----------------------------
# Nueva función solicitada: obtener reportes con nombre de tipo
# ----------------------------
def obtener_reportes_con_nombre_tipo():
    """
    Obtiene los reportes junto con el nombre del tipo (unión con tabla tipo).
    
    Returns:
        Lista de diccionarios con los datos de reportes y nombre_tipo
    """
    try:
        supabase = get_connection()

        # 🔵 Hacer un JOIN manual usando select anidado
        response = supabase.table("reporte").select(
            """
            id_reporte,
            fecha_creacion,
            fecha_resuelto,
            latitud,
            longitud,
            codigo_postal,
            fk_reporte_tipo(
                nombre_tipo
            )
            """
        ).execute()

        if response and hasattr(response, "data") and response.data:
            reportes = []
            for reporte in response.data:
                nombre_tipo = None
                # fk_reporte_tipo vendrá como un diccionario si el join fue correcto
                if isinstance(reporte.get("fk_reporte_tipo"), dict):
                    nombre_tipo = reporte["fk_reporte_tipo"].get("nombre_tipo")
                
                reporte["nombre_tipo"] = nombre_tipo
                # (Opcional) eliminar fk_reporte_tipo original si no lo quieres
                reporte.pop("fk_reporte_tipo", None)
                
                reportes.append(reporte)

            return reportes
        else:
            print("No se encontraron datos de reportes o respuesta inesperada.")
            return []
        
    except Exception as e:
        print(f"Error al obtener reportes con nombre de tipo: {e}")
        return []

def obtener_conteo_eventos_por_tipo_y_estado():
    """
    Suma el número de eventos agrupados por tipo de reporte (nombre_tipo) 
    y separados entre resueltos y no resueltos.
    
    Returns:
        Diccionario con nombre_tipo como clave y conteos de eventos como valores
    """
    try:
        supabase = get_connection()

        response = supabase.table("reporte").select(
            """
            num_eventos,
            fecha_resuelto,
            fk_reporte_tipo(
                nombre_tipo
            )
            """
        ).execute()

        if response and hasattr(response, "data") and response.data:
            conteo_eventos = {}

            for reporte in response.data:
                # Obtener tipo de reporte
                nombre_tipo = "Otro"
                if isinstance(reporte.get("fk_reporte_tipo"), dict):
                    nombre_tipo = reporte["fk_reporte_tipo"].get("nombre_tipo", "Otro")
                
                # Obtener cantidad de eventos
                eventos = reporte.get("num_eventos", 0) or 0

                # Saber si es resuelto o no
                resuelto = reporte.get("fecha_resuelto") is not None

                # Inicializar si no existe
                if nombre_tipo not in conteo_eventos:
                    conteo_eventos[nombre_tipo] = {"resueltos": 0, "no_resueltos": 0}

                # Sumar en el contador correcto
                if resuelto:
                    conteo_eventos[nombre_tipo]["resueltos"] += eventos
                else:
                    conteo_eventos[nombre_tipo]["no_resueltos"] += eventos

            return conteo_eventos
        
        else:
            print("No se encontraron datos de reportes o respuesta inesperada.")
            return {}
        
    except Exception as e:
        print(f"Error al obtener conteo de eventos por tipo y estado: {e}")
        return {}


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
    
def obtener_conteo_por_tipo_y_estado():
    """
    Cuenta los reportes por tipo y estado (resuelto/no resuelto).
    
    Returns:
        Diccionario donde cada clave es un tipo de reporte, 
        y su valor es otro diccionario con el conteo de resueltos y no resueltos.
    """
    try:
        reportes = obtener_reportes()
        
        conteo = {}
        
        for reporte in reportes:
            tipo = reporte.get("fk_reporte_tipo", "Otro")
            resuelto = bool(reporte.get("fecha_resuelto"))
            
            # Inicializar estructura si no existe
            if tipo not in conteo:
                conteo[tipo] = {"resueltos": 0, "no_resueltos": 0}
            
            # Sumar al conteo correspondiente
            if resuelto:
                conteo[tipo]["resueltos"] += 1
            else:
                conteo[tipo]["no_resueltos"] += 1
        
        return conteo

    except Exception as e:
        print(f"Error al contar reportes por tipo y estado: {e}")
        return {}

# Si quieres probar la conexión directamente al ejecutar este archivo
if __name__ == "__main__":
    try:
        connection = get_connection()
        print("Conexión a Supabase establecida correctamente")
        
        reportes = obtener_reportes()
        print(f"Se obtuvieron {len(reportes)} reportes")
    except Exception as e:
        print(f"Error al conectar con Supabase: {e}")