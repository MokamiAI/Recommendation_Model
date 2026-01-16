# scraper/search.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (InsuranceResearchBot/1.0)"
}


def search_company_products(company_name: str, limit: int = 5) -> list[str]:
    """
    Search for public insurance product pages using company name.
    """

    query = quote(f"{company_name} insurance products South Africa")
    url = f"https://duckduckgo.com/html/?q={query}"

    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    links: list[str] = []

    for a in soup.select("a.result__a"):
        href = a.get("href")
        if href and href.startswith("http"):
            links.append(href)

        if len(links) >= limit:
            break

    return links
