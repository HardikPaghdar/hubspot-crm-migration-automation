# Architecture

## Flow

1. **Input:** CSV export from a source CRM or spreadsheet.
2. **Normalize:** standardize common column aliases, trim strings, lowercase email addresses, and normalize phone punctuation.
3. **Validate:** require an email and check basic email syntax for this reference workflow.
4. **Deduplicate:** keep the first occurrence of each non-empty email and report subsequent rows as duplicates.
5. **Preview:** show accepted, duplicate, and rejected records before any external write.
6. **Apply (CLI only):** after explicit confirmation, send accepted contacts to HubSpot's CRM v3 batch-create endpoint.
7. **Report:** write a JSON report with counts, rejected rows, duplicate rows, and API errors.

## Design decisions

- Dry-run is the default; the dashboard never writes to HubSpot.
- A live run requires both `--apply` and `HUBSPOT_CONFIRM_LIVE_MIGRATION=YES`.
- API tokens are read from environment variables and must never be committed.
- This starter currently creates **contacts only**. Companies, deals, notes, associations, update/upsert behavior, and source-system-specific field mappings need to be scoped and implemented for the target account before production use.
- Local duplicate detection is not a substitute for checking records already in HubSpot. Run a controlled pilot and reconcile against the target CRM before a full migration.
- Review lifecycle-stage values and custom property names against the target HubSpot portal before applying data.

## Production hardening checklist

- Add idempotency and remote duplicate checks.
- Persist checkpoints and source-to-target record IDs.
- Add bounded exponential backoff and `Retry-After` handling for rate limits.
- Implement per-record outcomes for partial batch failures.
- Add field mapping per source and custom property validation.
- Add integration tests against a sandbox HubSpot portal.
- Confirm consent, retention, access, and rollback requirements with the data owner.
