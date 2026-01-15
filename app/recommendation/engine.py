from typing import Dict


def score_product(product: Dict, user: Dict) -> Dict:
    score = 0
    reasons = []

    # -------------------------------------------------
    # Budget
    # -------------------------------------------------
    premium = product.get("premium_min")

    if premium and premium <= user["monthly_budget"]:
        score += 30
        reasons.append("Within your monthly budget")

    # -------------------------------------------------
    # Age eligibility
    # -------------------------------------------------
    if (
        product.get("target_age_min") is not None
        and product.get("target_age_max") is not None
        and product["target_age_min"] <= user["age"] <= product["target_age_max"]
    ):
        score += 20
        reasons.append("Suitable for your age")

    # -------------------------------------------------
    # Province
    # -------------------------------------------------
    provinces = product.get("provinces_available")

    if provinces is None or user["province"] in provinces:
        score += 10
        reasons.append("Available in your province")

    # -------------------------------------------------
    # Underwriting vs risk preference
    # -------------------------------------------------
    underwriting = product.get("underwriting_type")

    if user["risk_preference"] == "low" and underwriting == "full_underwriting":
        score += 10
        reasons.append("Strong underwriting (lower risk)")

    if user["risk_preference"] == "high" and underwriting == "guaranteed_acceptance":
        score += 10
        reasons.append("Easy acceptance (higher risk tolerance)")

    # -------------------------------------------------
    # Compliance trust
    # -------------------------------------------------
    if product.get("fsca_compliant"):
        score += 5
        reasons.append("FSCA compliant")

    if product.get("treat_customers_fairly"):
        score += 5
        reasons.append("Treats customers fairly")

    return {
        "score": score,
        "reasons": reasons
    }
