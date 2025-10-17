from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Tuple

from .storage import FileStorage, Prompt


_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9_]+", re.UNICODE)


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in _WORD_RE.findall(text)]


def bm25_rank(query: str, documents: List[Prompt], k1: float = 1.5, b: float = 0.75) -> List[Tuple[Prompt, float]]:
    tokens = tokenize(query)
    if not tokens:
        return [(d, 0.0) for d in documents]

    N = len(documents)
    avgdl = sum(len(tokenize(d.prompt)) for d in documents) / (N or 1)

    # Build inverted index
    df: Dict[str, int] = defaultdict(int)
    tfs: List[Counter] = []
    for d in documents:
        toks = tokenize(d.prompt + "\n" + d.act)
        tf = Counter(toks)
        tfs.append(tf)
        for term in tf:
            df[term] += 1

    scores: List[float] = [0.0] * N
    for term in tokens:
        n_qi = df.get(term, 0)
        if n_qi == 0:
            continue
        idf = math.log(1 + (N - n_qi + 0.5) / (n_qi + 0.5))
        for i, d in enumerate(documents):
            f_qi_D = tfs[i].get(term, 0)
            if f_qi_D == 0:
                continue
            dl = sum(tfs[i].values())
            denom = f_qi_D + k1 * (1 - b + b * dl / (avgdl or 1))
            score = idf * (f_qi_D * (k1 + 1)) / (denom or 1)
            scores[i] += score

    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return ranked


def search(query: str, storage: FileStorage | None = None, top_k: int = 10) -> List[Tuple[Prompt, float]]:
    storage = storage or FileStorage()
    docs = storage.list()
    return bm25_rank(query, docs)[:top_k]
