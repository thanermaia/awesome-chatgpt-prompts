from __future__ import annotations

import re
from typing import Dict


_PII_PATTERNS = {
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", re.IGNORECASE),
    "phone": re.compile(r"\b\+?\d[\d\s().-]{7,}\b"),
}


def scrub_pii(text: str, replacement: str = "[REDACTED]") -> str:
    for _, pattern in _PII_PATTERNS.items():
        text = pattern.sub(replacement, text)
    return text


BRAND_POLICY = {
    "forbidden_claims": [
        "garantimos resultados",  # claims legais absolutas
        "100% seguro",
    ],
}


def enforce_brand_policy(text: str, policy: Dict | None = None) -> str:
    policy = policy or BRAND_POLICY
    for claim in policy.get("forbidden_claims", []):
        text = re.sub(re.escape(claim), "[REMOVIDO]", text, flags=re.IGNORECASE)
    return text
