from app.db.supabase_client import supabase

def insert_features(product_id: str, features: list[dict]):
    rows = []

    for f in features:
        rows.append({
            "product_id": product_id,
            "feature_type": f["feature_type"],  # must match CHECK constraint
            "feature_name": f["feature_name"],
            "feature_description": f.get("feature_description"),
            "feature_value": f.get("feature_value"),
            "is_standard": f.get("is_standard", True),
            "additional_cost": f.get("additional_cost")
        })

    if rows:
        supabase.table("product_features").insert(rows).execute()
