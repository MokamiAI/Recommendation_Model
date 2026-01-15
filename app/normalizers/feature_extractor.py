FEATURE_KEYWORDS = {
    "coverage": ["cover", "includes", "insured for"],
    "exclusion": ["not covered", "excludes", "does not cover"],
    "benefit": ["benefit", "reward", "advantage"],
    "value_added": ["free", "included", "24/7"]
}

def extract_features(raw_text: str) -> list[dict]:
    features = []

    lines = raw_text.split(".")
    for line in lines:
        l = line.lower()

        for feature_type, keywords in FEATURE_KEYWORDS.items():
            if any(k in l for k in keywords):
                features.append({
                    "feature_type": feature_type,
                    "feature_name": line.strip()[:120],
                    "feature_description": line.strip()
                })

    return features
