# scraper/page_scraper.py

import requests
from datetime import datetime
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (InsuranceResearchBot/1.0)"
}


def extract_visible_text(html: str) -> str:
    """
    Extract readable text from HTML.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove scripts & styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())


def scrape_public_page(company_name: str, url: str) -> dict:
    """
    Scrape a publicly accessible insurance-related page.
    """

    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    raw_text = extract_visible_text(response.text)

    return {
        "company_name": company_name,
        "product_name": f"{company_name} Insurance Product",
        "product_page_url": url,
        "raw_text": raw_text,
        "scraped_at": datetime.utcnow().isoformat()
    }
