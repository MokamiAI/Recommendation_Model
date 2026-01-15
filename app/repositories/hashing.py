# app/repositories/hashing.py

import hashlib
import json


def generate_data_hash(payload: dict) -> str:
    """
    Generates a stable SHA-256 hash for a product payload.
    Used to detect changes between scrapes.
    """
    normalized = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
