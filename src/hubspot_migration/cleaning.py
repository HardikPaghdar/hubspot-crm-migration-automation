"""Normalization and validation helpers for contact CSV rows."""
from __future__ import annotations
import re
from typing import Any


def _text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if value != value:
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def normalize_email(value: Any) -> str:
    return _text(value).lower()


def normalize_phone(value: Any) -> str:
    """Keep a leading plus and digits; formatting only, not country validation."""
    raw = _text(value)
    if not raw:
        return ""
    digits = re.sub(r"\D", "", raw)
    return f"+{digits}" if raw.startswith("+") and digits else digits


def normalize_contact(row: dict[str, Any]) -> dict[str, str]:
    """Map common source CRM headers to HubSpot-style contact property names."""
    normalized = {str(k).strip().lower(): _text(v) for k, v in row.items()}
    aliases = {
        "first name": "firstname", "first_name": "firstname", "firstname": "firstname",
        "last name": "lastname", "last_name": "lastname", "lastname": "lastname",
        "e-mail": "email", "email address": "email", "email": "email",
        "company name": "company", "company": "company",
        "phone number": "phone", "phone": "phone",
        "job title": "jobtitle", "job_title": "jobtitle", "jobtitle": "jobtitle",
        "website": "website", "lifecycle stage": "lifecyclestage", "lifecyclestage": "lifecyclestage",
    }
    output: dict[str, str] = {}
    for source_key, value in normalized.items():
        target = aliases.get(source_key, source_key.replace(" ", "_"))
        output[target] = value
    output["email"] = normalize_email(output.get("email", ""))
    output["phone"] = normalize_phone(output.get("phone", ""))
    return output


def validate_contact(row: dict[str, str]) -> list[str]:
    """Return validation issue codes for the supported contact workflow."""
    errors: list[str] = []
    email = row.get("email", "")
    if not email:
        errors.append("missing_email")
    elif not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        errors.append("invalid_email")
    return errors
