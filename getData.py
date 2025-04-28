response = (
    supabase.table("planets")
    .select("*")
    .execute()
)