# CRM workflow designs

This document separates the working migration preview from the workflow designs that should be configured and verified in the target HubSpot portal. The current code implements CSV contact preparation and opt-in contact batch creation; it does **not** create HubSpot-native workflows automatically.

## Workflow A — Lead assignment

**Trigger:** a contact is created or a qualifying lead property changes.

**Proposed steps:**
1. Validate required routing properties (country/region, product interest, and lifecycle stage).
2. Assign an owner using an agreed territory or round-robin rule.
3. Set an assignment timestamp and source campaign property.
4. Notify the assigned owner when routing succeeds.
5. Route incomplete records to a CRM operations review queue instead of guessing an owner.

**Acceptance checks:** each eligible test contact receives exactly one owner; incomplete records are visible to operations; reruns do not create duplicate tasks or notifications.

## Workflow B — Follow-up task creation

**Trigger:** a qualified lead is created or a lead reaches the agreed stage.

**Proposed steps:**
1. Check consent, suppression, and communication preferences before any outreach action.
2. Create a follow-up task with a due date based on the team's SLA.
3. Notify the owner through the approved channel.
4. Stop or branch when the contact replies, is disqualified, or is opted out.
5. Record a reason when the task cannot be created.

**Acceptance checks:** no follow-up is sent to opted-out contacts; task creation is idempotent; owners can see task status and exception reasons.

## Workflow C — Deal-stage hygiene

**Trigger:** a deal moves to a configured pipeline stage.

**Proposed steps:**
1. Validate required deal properties for that stage.
2. If fields are missing, notify the owner and create a remediation task.
3. If the stage is valid, notify the next responsible team and update the next-action date.
4. Log stage changes and failed actions for audit/reconciliation.

**Acceptance checks:** invalid transitions are visible; notifications go to the expected team; repeated events do not create duplicate tasks.

## Workflow D — Migration exception handling

**Trigger:** a row fails validation, is identified as a duplicate in the source file, or an API batch fails.

**Proposed steps:**
1. Keep the original row number and source reference in the migration report.
2. Classify the exception (missing email, invalid email, duplicate source email, API failure).
3. Export exceptions for review; do not silently discard them.
4. Retry only after the cause is understood and the row has been approved.

**Current implementation:** local duplicate and validation exceptions are included in the JSON report. API errors are summarized by batch. Fine-grained per-record reconciliation and persistent retry checkpoints remain future work.

## Rollout plan

1. Confirm business rules, field ownership, consent, and SLAs with stakeholders.
2. Configure workflows in a sandbox portal using synthetic test records.
3. Test positive, negative, duplicate-event, and opt-out scenarios.
4. Review logs and owner assignments with business users.
5. Promote changes with approval and monitor the first production cohort.
