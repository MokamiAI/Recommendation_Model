# app/scraper.py

import requests
from datetime import datetime
from typing import List, Dict

from app.utils import extract_visible_text
from app.repositories.company_repo import get_active_companies_with_websites

HEADERS = {
    "User-Agent": "Mozilla/5.0 (InsuranceResearchBot/1.0)"
}

REQUEST_TIMEOUT = 30


def fetch_page(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text


def scrape_company_website(company: Dict) -> Dict:
    """
    Scrape a company's website homepage.
    """

    html = fetch_page(company["website_url"])
    raw_text = extract_visible_text(html)

    return {
        "company_id": company["company_id"],
        "company_name": company["company_name"],
        "product_name": f"{company['company_name']} Insurance Products",
        "product_page_url": company["website_url"],
        "raw_text": raw_text,
        "scraped_at": datetime.utcnow().isoformat()
    }


def scrape_all_companies_from_db() -> List[Dict]:
    """
    Fetch active companies from DB and scrape their websites.
    """

    companies = get_active_companies_with_websites()
    results = []

    for company in companies:
        try:
            payload = scrape_company_website(company)
            results.append(payload)
        except Exception as e:
            results.append({
                "company_id": company.get("company_id"),
                "company_name": company.get("company_name"),
                "error": str(e)
            })

    return results
