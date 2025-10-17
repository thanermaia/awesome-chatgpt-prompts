from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass
class Prompt:
    id: str
    act: str
    prompt: str
    version: int = 1
    created_at: float = time.time()
    updated_at: float = time.time()
    tags: Optional[List[str]] = None


class FileStorage:
    def __init__(self, root_dir: str = "data/prompts") -> None:
        self.root_dir = root_dir
        os.makedirs(self.root_dir, exist_ok=True)

    def _path(self, prompt_id: str, version: int) -> str:
        safe_id = prompt_id.replace("/", "_")
        return os.path.join(self.root_dir, f"{safe_id}_v{version}.json")

    def list(self) -> List[Prompt]:
        prompts: List[Prompt] = []
        for name in sorted(os.listdir(self.root_dir)):
            if not name.endswith(".json"):
                continue
            path = os.path.join(self.root_dir, name)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                prompts.append(Prompt(**data))
        return prompts

    def load_latest(self, prompt_id: str) -> Optional[Prompt]:
        versions: List[int] = []
        for name in os.listdir(self.root_dir):
            if name.startswith(prompt_id) and name.endswith(".json"):
                try:
                    v = int(name.rsplit("_v", 1)[-1].split(".")[0])
                    versions.append(v)
                except Exception:
                    continue
        if not versions:
            return None
        latest_v = max(versions)
        path = self._path(prompt_id, latest_v)
        with open(path, "r", encoding="utf-8") as f:
            return Prompt(**json.load(f))

    def save_new_version(self, prompt: Prompt) -> Prompt:
        latest = self.load_latest(prompt.id)
        next_version = 1 if latest is None else latest.version + 1
        prompt.version = next_version
        prompt.updated_at = time.time()
        prompt.created_at = time.time() if latest is None else latest.created_at
        path = self._path(prompt.id, prompt.version)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(prompt), f, ensure_ascii=False, indent=2)
        return prompt

    def get(self, prompt_id: str, version: Optional[int] = None) -> Optional[Prompt]:
        if version is None:
            return self.load_latest(prompt_id)
        path = self._path(prompt_id, version)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return Prompt(**json.load(f))
