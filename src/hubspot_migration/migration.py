"""End-to-end CSV contact migration orchestration."""
from typing import Any
from hubspot_migration.cleaning import normalize_contact, validate_contact
from hubspot_migration.dedupe import find_duplicate_emails

HUBSPOT_PROPERTIES = {"email", "firstname", "lastname", "company", "phone", "website", "jobtitle", "lifecyclestage"}


def prepare_contacts(source_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Clean, validate and de-duplicate contacts without making network calls."""
    normalized = [normalize_contact(row) for row in source_rows]
    duplicates = find_duplicate_emails(normalized)
    ready, rejected, duplicate_rows = [], [], []
    for index, row in enumerate(normalized):
        if index in duplicates:
            duplicate_rows.append({"row_number": index + 2, "reason": "duplicate_email", "record": row})
            continue
        errors = validate_contact(row)
        if errors:
            rejected.append({"row_number": index + 2, "reasons": errors, "record": row})
            continue
        ready.append({key: value for key, value in row.items() if key in HUBSPOT_PROPERTIES and value != ""})
    return {"source_count": len(source_rows), "ready": ready, "rejected": rejected, "duplicates": duplicate_rows}
