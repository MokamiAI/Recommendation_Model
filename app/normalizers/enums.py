# app/normalizers/enums.py

PRODUCT_CATEGORY_MAP = {
    "car": "vehicle",
    "motor": "vehicle",
    "auto": "vehicle",
    "vehicle": "vehicle",

    "funeral": "funeral",

    "life": "life",
    "death": "life",

    "health": "health",
    "medical": "health",

    "travel": "travel",

    "home": "home",
    "house": "home",
    "household": "home",
    "property": "home",

    "business": "business",
    "commercial": "business",

    "agriculture": "agriculture",
    "farm": "agriculture",

    "marine": "marine"
}

UNDERWRITING_MAP = {
    "no medical": "guaranteed_acceptance",
    "no-medical": "guaranteed_acceptance",
    "guaranteed acceptance": "guaranteed_acceptance",

    "simplified": "simplified",

    "full underwriting": "full_underwriting",
    "medical required": "full_underwriting"
}

PREMIUM_FREQUENCY_KEYWORDS = {
    "per month": "monthly",
    "monthly": "monthly",

    "per year": "annual",
    "annual": "annual",
    "yearly": "annual",

    "once off": "single",
    "single premium": "single"
}
