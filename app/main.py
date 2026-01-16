from fastapi import FastAPI, HTTPException, Response

# --------------------------------------------------
# INGESTION (ADMIN / OPTIONAL)
# --------------------------------------------------
from app.schemas.ingestion import RawProductIn
from app.normalizers.product_normalizer import normalize_product
from app.normalizers.feature_extractor import extract_features
from app.repositories.company_repo import (
    get_or_create_company,
    get_active_companies
)
from app.repositories.product_repo import upsert_insurance_product
from app.repositories.features_repo import insert_features

# --------------------------------------------------
# SCRAPING
# --------------------------------------------------
from app.scraper.search import search_company_products
from app.scraper.page_scraper import scrape_public_page

# --------------------------------------------------
# RECOMMENDATION
# --------------------------------------------------
from app.schemas.recommendation import (
    RecommendationInput,
    RecommendationResponse
)
from app.recommendation.needs_engine import recommend_policies


app = FastAPI(
    title="Insurance Recommendation Engine",
    version="1.0.0"
)

# --------------------------------------------------
# BASIC ROUTES
# --------------------------------------------------
@app.get("/")
def root():
    return {"status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


# --------------------------------------------------
# MANUAL INGESTION (ADMIN / TESTING)
# --------------------------------------------------
@app.post("/ingest-raw")
def ingest_raw_product(raw: RawProductIn):
    """
    Manually ingest raw product text.
    """

    try:
        normalized = normalize_product(raw.dict())
        features = extract_features(raw.raw_text)

        company_id = get_or_create_company(raw.company_name)

        product_id = upsert_insurance_product(
            company_id=company_id,
            product=normalized
        )

        insert_features(product_id, features)

        return {
            "status": "ingested",
            "product_id": product_id,
            "features_created": len(features)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------------------------------
# 🔍 AUTO SCRAPE (COMPANY-BASED)
# --------------------------------------------------
@app.post("/scrape/auto")
def auto_scrape():
    """
    Automatically scrape insurance products
    for all active companies in the database.
    """

    companies = get_active_companies()
    results = []

    for company in companies:
        company_name = company["company_name"]

        try:
            urls = search_company_products(company_name)

            for url in urls:
                raw_text = scrape_public_page(url)

                normalized = normalize_product({
                    "company_name": company_name,
                    "raw_text": raw_text,
                    "source_url": url
                })

                features = extract_features(raw_text)

                company_id = get_or_create_company(company_name)

                product_id = upsert_insurance_product(
                    company_id=company_id,
                    product=normalized
                )

                insert_features(product_id, features)

                results.append({
                    "company": company_name,
                    "product_id": product_id
                })

        except Exception as e:
            results.append({
                "company": company_name,
                "error": str(e)
            })

    return {
        "status": "completed",
        "items_processed": len(results),
        "results": results
    }


# --------------------------------------------------
# 🎯 NEEDS-BASED RECOMMENDATION (CORE FEATURE)
# --------------------------------------------------
@app.post(
    "/recommend",
    response_model=RecommendationResponse
)
def recommend(input: RecommendationInput):
    """
    Needs-based insurance recommendation.

    • User submits personal details
    • System determines insurance needs
    • Returns ONLY recommended products
    • No user data is echoed back
    """

    try:
        engine_result = recommend_policies(input.dict())

        return {
            "recommended_policies": engine_result["recommended_policies"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
