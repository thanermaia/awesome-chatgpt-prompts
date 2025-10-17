from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from .guardrails import scrub_pii, enforce_brand_policy


@dataclass
class ProviderResponse:
    text: str
    meta: Dict


class EchoProvider:
    def __init__(self) -> None:
        pass

    def complete(self, prompt: str, **kwargs) -> ProviderResponse:
        text = prompt
        text = scrub_pii(text)
        text = enforce_brand_policy(text)
        return ProviderResponse(text=text, meta={"provider": "echo"})
