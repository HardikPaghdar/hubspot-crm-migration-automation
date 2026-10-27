"""Local duplicate detection helpers."""
from collections.abc import Iterable
from typing import Any


def find_duplicate_emails(rows: Iterable[dict[str, Any]]) -> set[int]:
    """Return zero-based indexes that repeat an earlier non-empty email."""
    seen: set[str] = set()
    duplicates: set[int] = set()
    for index, row in enumerate(rows):
        email = str(row.get("email", "") or "").strip().lower()
        if not email:
            continue
        if email in seen:
            duplicates.add(index)
        else:
            seen.add(email)
    return duplicates
