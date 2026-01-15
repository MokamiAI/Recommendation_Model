from pydantic import BaseModel, Field
from typing import List, Literal


# --------------------------------------------------
# USER INPUT (REQUEST)
# --------------------------------------------------
class RecommendationInput(BaseModel):
    age: int = Field(..., ge=18, le=100)
    monthly_budget: float = Field(..., gt=0)
    has_dependants: bool
    owns_car: bool
    employment_risk: Literal["low", "medium", "high"]


# --------------------------------------------------
# RECOMMENDATION CARD
# --------------------------------------------------
class RecommendationItem(BaseModel):
    policy_type: str
    company: str
    confidence_score: int
    priority_band: Literal["high", "medium", "low"]
    match_label: str
    description: str
    best_for: List[str]
    why_this_matches_you: List[str]
    coverage_amount: float
    coverage_currency: str = "ZAR"
    premium_amount: float
    premium_frequency: str


# --------------------------------------------------
# API RESPONSE
# --------------------------------------------------
class RecommendationResponse(BaseModel):
    recommended_policies: List[RecommendationItem]
