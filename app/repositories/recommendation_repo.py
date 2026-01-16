from app.db.supabase_client import supabase


def fetch_candidate_products(product_category: str):
    result = (
        supabase
        .from_("active_insurance_products")
        .select("*")
        .eq("product_category", product_category)
        .execute()
    )

    return result.data or []
