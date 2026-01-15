# scraper/company_name_scraper.py

from app.scraper.search import search_company_products
from app.scraper.page_scraper import scrape_public_page
from app.repositories.company_repo import get_active_companies


def scrape_by_company_name():
    """
    Scrape insurance products using company names instead of direct URLs.
    """

    companies = get_active_companies()
    results = []

    for company in companies:
        company_name = company["company_name"]

        try:
            urls = search_company_products(company_name)

            for url in urls:
                try:
                    payload = scrape_public_page(company_name, url)
                    results.append(payload)
                except Exception as e:
                    results.append({
                        "company_name": company_name,
                        "url": url,
                        "error": str(e)
                    })

        except Exception as e:
            results.append({
                "company_name": company_name,
                "error": str(e)
            })

    return results
