import re
from app.normalizers.enums import (
    PRODUCT_CATEGORY_MAP,
    UNDERWRITING_MAP,
    PREMIUM_FREQUENCY_KEYWORDS,
)

def normalize_product(raw: dict) -> dict:
    text = (raw.get("raw_text") or "").lower()

    product = {
        "product_name": raw.get("product_name"),
        "source_url": raw.get("product_page_url"),
        "coverage_description": raw.get("product_summary"),
    }

    # Product category
    for k, v in PRODUCT_CATEGORY_MAP.items():
        if k in text:
            product["product_category"] = v
            break

    # Premium frequency
    for k, v in PREMIUM_FREQUENCY_KEYWORDS.items():
        if k in text:
            product["premium_frequency"] = v
            break

    # Underwriting type
    for k, v in UNDERWRITING_MAP.items():
        if k in text:
            product["underwriting_type"] = v
            break

    # Waiting period
    wp = re.search(r"waiting\s*period.*?(\d+)\s*days", text)
    if wp:
        product["waiting_period_days"] = int(wp.group(1))

    # Age limits
    age = re.search(r"ages?\s*(\d+)\s*-\s*(\d+)", text)
    if age:
        product["target_age_min"] = int(age.group(1))
        product["target_age_max"] = int(age.group(2))

    return product
