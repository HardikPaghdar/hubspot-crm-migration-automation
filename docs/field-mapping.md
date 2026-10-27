# Field mapping guide

The example mapping in `config/field_mapping.json` is a starting point, not a universal mapping. Confirm source field names, HubSpot property internal names, required fields, and permitted values with the target portal administrator.

| Source header examples | HubSpot property | Handling |
| --- | --- | --- |
| `Email Address`, `E-mail`, `email` | `email` | Trim, lowercase, basic format validation; required by this demo |
| `First Name`, `first_name` | `firstname` | Trim whitespace |
| `Last Name`, `last_name` | `lastname` | Trim whitespace |
| `Company Name`, `company` | `company` | Trim whitespace; association to a company record is not created by this demo |
| `Phone Number`, `phone` | `phone` | Keep digits and a leading plus if present; no country-specific validation |
| `Job Title`, `job_title` | `jobtitle` | Trim whitespace |
| `Website` | `website` | Passed through as text; validate URL policy before production |
| `Lifecycle Stage` | `lifecyclestage` | Must be checked against values configured in the target portal |

## Before applying a mapping

- Agree how blank source values should be handled (leave unchanged, clear, or reject).
- Confirm custom properties and internal names exist in the destination portal.
- Decide how source IDs are retained for reconciliation and future updates.
- Identify whether contacts should be associated with companies and deals, and define association rules.
- Run a representative sample through dry-run and review exceptions with the data owner.
