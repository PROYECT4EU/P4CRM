# P4CRM data model — v0.1

This document defines the first logical model for P4CRM. The machine-readable contract lives in [`schemas/p4crm-v0.1.json`](../schemas/p4crm-v0.1.json).

## Entity map

```text
ORGANISATIONS
  | 1
  |----< CONTACT_POINTS
  |----< PEOPLE
  |----< PROSPECTS >---- PROJECTS
  |----< OPPORTUNITIES >- PROJECTS

CONTACT_POINTS
  |----< CONSENTS
  |----< SUPPRESSIONS
  |----< INTERACTIONS
  |----< DATA_TRANSFERS

SOURCES
  |----< CONTACT_POINTS
  |----< PROSPECTS

CAMPAIGNS
  |----< INTERACTIONS

CONSENTS
  |----< DATA_TRANSFERS
```

## 1. ORGANISATIONS

Represents a legal or institutional organisation: school, association, public administration, company, NGO, university, cultural entity, etc.

Primary key: `organisation_id`

Fields:

| Field | Required | Description |
|---|---:|---|
| `organisation_id` | yes | Stable P4CRM identifier |
| `name` | yes | Display name |
| `legal_name` | no | Legal name when known |
| `organisation_type` | yes | Controlled category |
| `tax_id` | no | Tax/legal identifier when legitimately required |
| `country` | no | Country |
| `region` | no | Region / autonomous community |
| `island` | no | Island |
| `municipality` | no | Municipality |
| `postal_code` | no | Postal code |
| `address` | no | Professional/public address |
| `website` | no | Canonical website |
| `status` | yes | `ACTIVE`, `INACTIVE` or `ARCHIVED` |
| `created_at` | yes | Creation timestamp |
| `updated_at` | yes | Last update timestamp |
| `notes` | no | Operational notes; avoid unnecessary personal data |

## 2. CONTACT_POINTS

Represents an address/channel through which an organisation or person can be contacted. An email existing here does not imply marketing permission.

Primary key: `contact_point_id`

Fields:

| Field | Required | Description |
|---|---:|---|
| `contact_point_id` | yes | Stable identifier |
| `organisation_id` | yes | Parent organisation |
| `person_id` | no | Optional named professional contact |
| `contact_type` | yes | `EMAIL`, `PHONE`, `WEB`, `POSTAL` |
| `value` | yes | Email, phone, URL, etc. |
| `label` | no | e.g. secretaría, dirección, orientación |
| `is_generic` | yes | Whether it identifies a generic institutional mailbox rather than a named person |
| `source_id` | yes | Provenance record |
| `verified_at` | no | Last source verification |
| `status` | yes | `ACTIVE`, `BOUNCED`, `INVALID`, `INACTIVE` |
| `created_at` | yes | Creation timestamp |
| `updated_at` | yes | Last update timestamp |

Recommended uniqueness rule: normalised `contact_type + value`, with merge/review logic rather than silent duplication.

## 3. PEOPLE

Optional professional person record. P4CRM should avoid creating a person record when a generic organisational contact is sufficient.

Primary key: `person_id`

Fields include `organisation_id`, `given_name`, `family_name`, `role`, `department`, `status`, `created_at`, `updated_at` and `notes`.

## 4. SOURCES

Records where data came from and when it was checked.

Primary key: `source_id`

Fields:

- `source_type`
- `source_name`
- `source_url`
- `publisher`
- `retrieved_at`
- `licence_or_terms`
- `notes`

Initial source types include public directories, organisation websites, direct contact, forms, referrals and existing relationships.

## 5. PROSPECTS

Represents a potential relationship between an organisation and a P4CRM project or programme. This is not a consent table.

Primary key: `prospect_id`

Important fields:

- `organisation_id`
- `project_code`
- `source_id`
- `segment`
- `priority`
- `relationship_status`
- `interests`
- `owner`
- `created_at`
- `updated_at`
- `notes`

A school can therefore be a PROYECT4 prospect even when every related consent remains `NOT_GRANTED`.

## 6. CONSENTS

Immutable/auditable permission events and current consent state.

Primary key: `consent_id`

Natural scope:

```text
contact_point_id + controller_code + purpose_code + channel
```

Fields:

- `consent_id`
- `contact_point_id`
- `controller_code`
- `purpose_code`
- `channel`
- `status`
- `granted_at`
- `revoked_at`
- `source_type`
- `form_id`
- `text_version`
- `privacy_version`
- `evidence_ref`
- `notes`

Initial purposes:

- `P4_EDUCATIONAL_RELATION`
- `SAN_BLAS_EDUCATIONAL_VISITS`

A future implementation should retain consent event history rather than overwriting the only proof of a previous state.

## 7. SUPPRESSIONS

Prevents communication even after a later re-import.

Primary key: `suppression_id`

Scope may be global or controller/purpose specific.

Fields include:

- `contact_point_id`
- `controller_code`
- `purpose_code`
- `channel`
- `reason`
- `suppressed_at`
- `source`
- `notes`

Examples of reasons: `UNSUBSCRIBED`, `OBJECTED`, `BOUNCE`, `INVALID`, `MANUAL_BLOCK`, `COMPLAINT`.

## 8. INTERACTIONS

Append-oriented log of relationship and communication events.

Primary key: `interaction_id`

Typical fields:

- `organisation_id`
- `contact_point_id`
- `project_code`
- `campaign_id`
- `interaction_type`
- `direction`
- `occurred_at`
- `outcome`
- `reference`
- `notes`

Examples: email sent, email clicked, form submitted, phone call, meeting, resource download, enquiry, participation.

## 9. CAMPAIGNS

Defines a communication initiative, not its recipient list.

Primary key: `campaign_id`

Fields include `name`, `project_code`, `purpose_code`, `channel`, `audience_definition`, `start_at`, `end_at`, `status`, `frequency_rule` and `notes`.

Audience generation must check consent/legal-basis rules and suppressions at send time.

## 10. DATA_TRANSFERS

Audit record for authorised communication of data from PROYECT4 to another controller/recipient.

Primary key: `transfer_id`

Fields:

- `contact_point_id`
- `from_controller_code`
- `to_controller_code`
- `purpose_code`
- `legal_basis`
- `consent_id`
- `transferred_at`
- `transfer_method`
- `receipt_ref`
- `status`
- `notes`

For the San Blas use case, a transfer should require a valid consent record for `SAN_BLAS_EDUCATIONAL_VISITS` before it can be marked `COMPLETED`.

## 11. PROJECTS

Registry of CRM-relevant initiatives and external collaborations.

Primary key: `project_code`

Initial records:

- `P4` — PROYECT4 institutional CRM
- `SAN_BLAS` — San Blas Reserva Ambiental educational relationship
- `GOFIODESIGN` — creative/material-production relationship, without implied marketing permission

The `controller_code` field must not be used to guess an unknown legal controller. Production configuration must identify controllers accurately.

## 12. OPPORTUNITIES

Tracks potential substantive collaborations with organisations.

Primary key: `opportunity_id`

Examples:

- sustainability programme;
- educational escape room;
- heritage project;
- entrepreneurship activity;
- social-relations / coexistence programme;
- case-based learning project.

Fields include `organisation_id`, `project_code`, `opportunity_type`, `theme`, `stage`, `estimated_start`, `owner`, `value_or_scope`, `created_at`, `updated_at` and `notes`.

## Data rules for v0.1

- Stable IDs are never recycled.
- Deletion is not used to represent an opt-out; suppression is retained.
- Sources are recorded before or with imported contact data.
- Interest tags do not imply permission.
- Consent is not inherited between controllers or purposes.
- A completed third-party transfer points back to the authorising consent.
- Production personal/contact data must never be committed to GitHub.
