# app/repositories/product_repo.py

from datetime import datetime
from app.db.supabase_client import supabase
from app.repositories.hashing import generate_data_hash


def upsert_insurance_product(company_id: str, product: dict) -> str:
    """
    Insert or update an insurance product.
    Uses data_hash to detect changes.
    Returns product_id.
    """

    # Generate data hash for change detection
    data_hash = generate_data_hash(product)

    # Try find existing product (by company + name)
    existing = (
        supabase
        .table("insurance_products")
        .select("product_id, data_hash")
        .eq("company_id", company_id)
        .eq("product_name", product.get("product_name"))
        .eq("is_active", True)
        .execute()
    )

    payload = {
        "company_id": company_id,
        "product_name": product.get("product_name"),
        "product_code": product.get("product_code"),
        "product_category": product.get("product_category"),
        "product_subcategory": product.get("product_subcategory"),
        "coverage_description": product.get("coverage_description"),
        "sum_assured_min": product.get("sum_assured_min"),
        "sum_assured_max": product.get("sum_assured_max"),
        "premium_frequency": product.get("premium_frequency"),
        "premium_min": product.get("premium_min"),
        "premium_max": product.get("premium_max"),
        "waiting_period_days": product.get("waiting_period_days"),
        "claims_process_description": product.get("claims_process_description"),
        "underwriting_type": product.get("underwriting_type"),
        "target_age_min": product.get("target_age_min"),
        "target_age_max": product.get("target_age_max"),
        "target_income_min": product.get("target_income_min"),
        "target_income_max": product.get("target_income_max"),
        "urban_rural_focus": product.get("urban_rural_focus"),
        "source_url": product.get("source_url") or product.get("product_page_url"),
        "last_scraped": datetime.utcnow().isoformat(),
        "data_hash": data_hash,
        "is_active": True
    }

    # ----------------------------------
    # UPDATE EXISTING PRODUCT
    # ----------------------------------
    if existing.data:
        existing_row = existing.data[0]

        # Skip update if nothing changed
        if existing_row["data_hash"] == data_hash:
            return existing_row["product_id"]

        updated = (
            supabase
            .table("insurance_products")
            .update(payload)
            .eq("product_id", existing_row["product_id"])
            .execute()
        )

        return updated.data[0]["product_id"]

    # ----------------------------------
    # INSERT NEW PRODUCT
    # ----------------------------------
    inserted = (
        supabase
        .table("insurance_products")
        .insert(payload)
        .execute()
    )

    return inserted.data[0]["product_id"]
