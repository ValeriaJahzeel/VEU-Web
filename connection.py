from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
   
supabase = create_client(supabase_url, supabase_key)

response = supabase.table("reporte").select("*").execute()

print("Respuesta completa:", response)
    
if response and hasattr(response, "data") and response.data:
    data = response.data
    print("Datos obtenidos:")
    for row in data:
        print(row)
else:
    print("No se encontraron datos o formato de respuesta inesperado.")