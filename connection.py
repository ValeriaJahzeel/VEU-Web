from supabase import create_client
import os
from dotenv import load_dotenv

def connection():
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("Error al conectar con la base de datos")
    
    supabase = create_client(supabase_url, supabase_key)
    return supabase
