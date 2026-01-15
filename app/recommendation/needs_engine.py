import os
from typing import Dict, List
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# SUPABASE (SERVICE ROLE)
# --------------------------------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL1")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY1")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Supabase credentials missing. "
        "Ensure SUPABASE_URL1 and SUPABASE_SERVICE_ROLE_KEY1 are set."
    )

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --------------------------------------------------
# FETCH ACTIVE PRODUCTS
# --------------------------------------------------
def fetch_active_products() -> List[Dict]:
    response = (
        supabase
        .table("insurance_products")
        .select(
            "product_name,"
            "provider,"
            "category,"
            "description,"
            "premium_amount,"
            "coverage_amount,"
            "frequency,"
            "eligibility"
        )
        .eq("active", True)
        .execute()
    )

    return response.data or []


# --------------------------------------------------
# SCORING LOGIC
# --------------------------------------------------
def score_product(product: Dict, profile: Dict) -> int:
    score = 0

    category = (product.get("category") or "").lower()
    premium = float(product.get("premium_amount") or 0)
    coverage = float(product.get("coverage_amount") or 0)
    eligibility = (product.get("eligibility") or "").lower()

    # -------------------------
    # CATEGORY RELEVANCE (40)
    # -------------------------
    if category == "life" and profile.get("has_dependants"):
        score += 40
    elif category == "accident" and profile.get("employment_risk") in ["medium", "high"]:
        score += 35
    elif category == "car" and profile.get("owns_car"):
        score += 40
    elif category == "funeral":
        score += 20

    # -------------------------
    # BUDGET FIT (25)
    # -------------------------
    budget = float(profile.get("monthly_budget") or 0)
    if budget > 0:
        if premium <= budget:
            score += 25
        elif premium <= budget * 1.3:
            score += 15

    # -------------------------
    # VALUE FOR MONEY (20)
    # -------------------------
    if premium > 0:
        ratio = coverage / premium
        if ratio >= 1000:
            score += 20
        elif ratio >= 500:
            score += 10

    # -------------------------
    # AGE ELIGIBILITY (15)
    # -------------------------
    if "age" in eligibility:
        score += 15

    return min(score, 100)


def priority_band(score: int) -> str:
    if score >= 80:
        return "high"
    if score >= 60:
        return "medium"
    return "low"


# --------------------------------------------------
# DYNAMIC EXPLANATION ENGINE
# --------------------------------------------------
def why_this_matters(
    category: str,
    score: int,
    profile: Dict,
    coverage: float,
    premium: float
) -> List[str]:

    reasons: List[str] = []
    band = priority_band(score)
    category = category.lower()

    # -------------------------
    # CATEGORY-SPECIFIC LOGIC
    # -------------------------
    if category == "accident":
        if profile.get("employment_risk") in ["medium", "high"]:
            reasons.append("Provides protection for higher daily risk exposure")

        if band == "high":
            reasons.append("Highly relevant based on your activity level")

    elif category == "life":
        if profile.get("has_dependants"):
            reasons.append("Helps secure your dependants’ financial future")

        if band == "high":
            reasons.append("Strong long-term financial protection")

    elif category == "car":
        if profile.get("owns_car"):
            reasons.append("Essential protection for vehicle ownership")

    elif category == "funeral":
        reasons.append("Helps reduce immediate financial burden on loved ones")
        if premium == 0:
            reasons.append("Includes coverage at no monthly cost")

    # -------------------------
    # VALUE-BASED LOGIC
    # -------------------------
    if premium > 0 and coverage / premium >= 800:
        reasons.append("Offers strong coverage relative to the premium")

    if premium <= float(profile.get("monthly_budget") or 0):
        reasons.append("Fits comfortably within your monthly budget")

    # -------------------------
    # CONFIDENCE TONE
    # -------------------------
    if band == "high":
        reasons.append("Strong overall match for your current needs")
    elif band == "medium":
        reasons.append("Reasonably aligned with your situation")

    # Deduplicate & limit length
    return list(dict.fromkeys(reasons))[:2]


def best_for_text(category: str) -> List[str]:
    return {
        "accident": ["Young professionals", "Working professionals"],
        "life": ["People with dependants", "Primary income earners"],
        "car": ["Vehicle owners", "Daily commuters"],
        "funeral": ["All households", "Budget-conscious families"]
    }.get(category.lower(), [])


# --------------------------------------------------
# MAIN ENGINE ENTRY POINT
# --------------------------------------------------
def recommend_policies(profile: Dict) -> Dict:
    products = fetch_active_products()
    scored: List[Dict] = []

    for product in products:
        score = score_product(product, profile)
        if score > 0:
            scored.append({
                "product": product,
                "score": score
            })

    if not scored:
        return {"recommended_policies": []}

    scored.sort(key=lambda x: x["score"], reverse=True)

    top = scored[0]
    second = scored[1] if len(scored) > 1 else None

    def format_output(item: Dict) -> Dict:
        p = item["product"]
        s = item["score"]

        return {
            "policy_type": p["product_name"],
            "company": p["provider"],
            "confidence_score": s,
            "priority_band": priority_band(s),
            "match_label": f"{s}% match",
            "description": p["description"],
            "best_for": best_for_text(p["category"]),
            "why_this_matches_you": why_this_matters(
                category=p["category"],
                score=s,
                profile=profile,
                coverage=float(p["coverage_amount"]),
                premium=float(p["premium_amount"])
            ),
            "coverage_amount": float(p["coverage_amount"]),
            "coverage_currency": "ZAR",
            "premium_amount": float(p["premium_amount"]),
            "premium_frequency": p["frequency"]
        }

    recommendations = [format_output(top)]
    if second:
        recommendations.append(format_output(second))

    return {
        "recommended_policies": recommendations
    }
