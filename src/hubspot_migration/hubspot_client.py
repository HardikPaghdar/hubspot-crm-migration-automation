"""Small HubSpot CRM API client for contact batch creation."""
from __future__ import annotations
import os
import time
from typing import Any
import requests


class HubSpotAPIError(RuntimeError):
    """Raised when HubSpot returns an unsuccessful API response."""


class HubSpotClient:
    def __init__(self, access_token: str | None = None, base_url: str | None = None) -> None:
        self.access_token = access_token or os.getenv("HUBSPOT_ACCESS_TOKEN", "")
        self.base_url = (base_url or os.getenv("HUBSPOT_API_BASE_URL", "https://api.hubapi.com")).rstrip("/")
        if not self.access_token:
            raise ValueError("HUBSPOT_ACCESS_TOKEN is required for live migration")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"})

    def create_contacts(self, contacts: list[dict[str, str]], batch_size: int = 100) -> dict[str, Any]:
        """Create contacts in batches; this method does not claim to upsert existing records."""
        if not 1 <= batch_size <= 100:
            raise ValueError("batch_size must be between 1 and 100")
        created = 0
        errors: list[dict[str, Any]] = []
        for start in range(0, len(contacts), batch_size):
            batch = contacts[start:start + batch_size]
            payload = {"inputs": [{"properties": contact} for contact in batch]}
            response = self.session.post(f"{self.base_url}/crm/v3/objects/contacts/batch/create", json=payload, timeout=30)
            if response.status_code == 429:
                time.sleep(2)
                response = self.session.post(f"{self.base_url}/crm/v3/objects/contacts/batch/create", json=payload, timeout=30)
            if not response.ok:
                errors.append({"batch_start": start, "status_code": response.status_code, "message": response.text[:1000]})
                continue
            body = response.json()
            created += len(body.get("results", []))
            if body.get("errors"):
                errors.extend({"batch_start": start, "message": item} for item in body["errors"])
        return {"created": created, "submitted": len(contacts), "errors": errors}
