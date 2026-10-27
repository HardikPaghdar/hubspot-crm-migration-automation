# Migration runbook

## Before migration

- Export a backup from the source CRM and confirm the record types in scope.
- Agree on a field mapping and required properties with the CRM owner.
- Run the preview against a small, sanitized CSV first.
- Review duplicate and rejected rows with the data owner.
- Create a HubSpot private app with only the scopes needed for the approved work.
- Use a test portal or a small pilot before a production batch.

## Preview

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .[dashboard,dev]
python -m hubspot_migration.cli sample_data/contacts.csv --report reports/preview.json
streamlit run app.py
```

## Live contact creation

Only after reviewing the report and confirming the target portal:

```bash
# Add these only to your local .env; never commit secrets.
HUBSPOT_ACCESS_TOKEN=your_private_app_token
HUBSPOT_CONFIRM_LIVE_MIGRATION=YES

python -m hubspot_migration.cli path/to/approved_contacts.csv --apply --report reports/live-run.json
```

The live command creates contacts; it does not update existing records or migrate companies, deals, notes, activities, or associations. Treat it as a starter implementation, not a one-click production migration.

## After migration

- Compare source, accepted, created, rejected, and duplicate counts.
- Inspect API errors and sample records in HubSpot.
- Validate property values, owner assignment, lifecycle stages, and associations.
- Save the report with the approved migration record and follow the organization's retention policy.
