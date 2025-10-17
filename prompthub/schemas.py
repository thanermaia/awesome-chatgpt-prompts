from __future__ import annotations

import json
from typing import Any, Dict, Tuple

try:
    import jsonschema  # type: ignore
except Exception:  # fallback minimal validator
    jsonschema = None


class SchemaValidator:
    def __init__(self, schema: Dict[str, Any]) -> None:
        self.schema = schema

    def validate(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        if jsonschema is None:
            # Minimal structural check
            if not isinstance(data, dict):
                return False, "data is not an object"
            return True, "ok"
        try:
            jsonschema.validate(instance=data, schema=self.schema)
            return True, "ok"
        except Exception as e:
            return False, str(e)
