from app.db.supabase_client import supabase


def find_active_products(policy_type: str):
    result = (
        supabase
        .from_("active_insurance_products")
        .select("product_id, product_name, product_category, premium_min, premium_max")
        .ilike("product_category", policy_type.split()[0].lower())
        .execute()
    )

    return result.data or []
