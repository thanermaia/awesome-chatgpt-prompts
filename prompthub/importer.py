from __future__ import annotations

import csv
import os
from typing import Iterable, Optional

from .storage import FileStorage, Prompt


def slugify(value: str) -> str:
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789-"
    value = value.strip().lower().replace(" ", "-")
    out = []
    for ch in value:
        if ch in allowed:
            out.append(ch)
        elif ch.isalnum():
            out.append(ch.lower())
        else:
            out.append("-")
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "prompt"


def import_from_csv(
    csv_path: str,
    storage: Optional[FileStorage] = None,
    id_prefix: Optional[str] = None,
) -> int:
    if storage is None:
        storage = FileStorage()
    if not os.path.exists(csv_path):
        raise FileNotFoundError(csv_path)

    num_imported = 0
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "act" not in reader.fieldnames or "prompt" not in reader.fieldnames:
            raise ValueError("CSV must contain 'act' and 'prompt' columns")
        for row in reader:
            act = (row.get("act") or "").strip()
            prompt_text = (row.get("prompt") or "").strip()
            if not act or not prompt_text:
                continue
            base_id = slugify(act)
            prompt_id = f"{id_prefix}-{base_id}" if id_prefix else base_id
            prompt = Prompt(id=prompt_id, act=act, prompt=prompt_text)
            storage.save_new_version(prompt)
            num_imported += 1
    return num_imported
