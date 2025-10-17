from __future__ import annotations

import os
from typing import List, Tuple

from .search import tokenize


class SimpleIndexer:
    def __init__(self, kb_dir: str = "knowledge_base") -> None:
        self.kb_dir = kb_dir
        os.makedirs(self.kb_dir, exist_ok=True)

    def _doc_paths(self) -> List[str]:
        files: List[str] = []
        for name in os.listdir(self.kb_dir):
            path = os.path.join(self.kb_dir, name)
            if os.path.isfile(path) and not name.startswith("."):
                files.append(path)
        return sorted(files)

    def load_docs(self) -> List[Tuple[str, str]]:
        docs: List[Tuple[str, str]] = []
        for path in self._doc_paths():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    docs.append((path, f.read()))
            except Exception:
                continue
        return docs

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        docs = self.load_docs()
        q_tokens = set(tokenize(query))
        scores: List[Tuple[str, float]] = []
        for path, content in docs:
            d_tokens = set(tokenize(content))
            overlap = len(q_tokens & d_tokens)
            length_norm = len(d_tokens) or 1
            score = overlap / length_norm
            scores.append((path, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]
