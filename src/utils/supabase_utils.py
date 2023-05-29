import os
from dotenv import load_dotenv
import supabase

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_api_key = os.getenv("SUPABASE_SERVICE_KEY")

client = supabase.Client(supabase_url, supabase_api_key)

def get_row_count():
    response = client.table('documents').select('id').execute()
    return len(response.data)