from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

from .providers import EchoProvider, ProviderResponse


@dataclass
class Variant:
    name: str
    render: Callable[[Dict], str]  # data -> prompt string


@dataclass
class ABResult:
    variant: str
    response: ProviderResponse


def run_ab_test(task_data: Dict, variants: List[Variant]) -> List[ABResult]:
    provider = EchoProvider()
    results: List[ABResult] = []
    for v in variants:
        prompt = v.render(task_data)
        resp = provider.complete(prompt)
        results.append(ABResult(variant=v.name, response=resp))
    random.shuffle(results)
    return results
