"""JSON report writer for migration runs."""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_report(result: dict[str, Any], path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {"generated_at": datetime.now(timezone.utc).isoformat(), **result}
    destination.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return destination
