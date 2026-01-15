# app/repositories/company_repo.py

from app.db.supabase_client import supabase


def get_or_create_company(company_name: str):
    """
    Fetch a company by name or create it if it does not exist.
    """

    existing = (
        supabase
        .table("insurance_companies")
        .select("company_id")
        .eq("company_name", company_name)
        .execute()
    )

    if existing.data:
        return existing.data[0]["company_id"]

    inserted = (
        supabase
        .table("insurance_companies")
        .insert({
            "company_name": company_name,
            "is_active": True
        })
        .execute()
    )

    return inserted.data[0]["company_id"]


def get_active_companies_with_websites():
    """
    Fetch active insurance companies that have website URLs.
    Used by the scraper.
    """

    result = (
        supabase
        .table("insurance_companies")
        .select(
            "company_id",
            "company_name",
            "website_url"
        )
        .eq("is_active", True)
        .not_.is_("website_url", None)
        .execute()
    )
    
def get_active_companies():
    result = (
        supabase
        .table("insurance_companies")
        .select("company_id, company_name")
        .eq("is_active", True)
        .execute()
    )

    return result.data or []

