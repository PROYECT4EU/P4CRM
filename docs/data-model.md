# P4CRM data model — v0.2

The machine-readable contract lives in [`schemas/p4crm-v0.2.json`](../schemas/p4crm-v0.2.json).

## Entity map

```text
ORGANISATIONS
  |----< ORGANISATION_IDENTIFIERS
  |----< CONTACT_POINTS ----< CONTACT_POINT_SOURCES
  |----< PEOPLE
  |----< PROSPECTS >---- PROJECTS
  |----< OPPORTUNITIES >- PROJECTS

SOURCES
  |----< IMPORT_BATCHES
  |----< CONTACT_POINT_SOURCES

CONTACT_POINTS
  |----< CONSENT_REQUESTS ----< CONSENT_REQUEST_SCOPES
  |----< CONSENTS ----< CONSENT_EVENTS
  |----< SUPPRESSIONS
  |----< INTERACTIONS
  |----< DATA_TRANSFERS

CAMPAIGNS
  |----< INTERACTIONS

CONSENTS
  |----< DATA_TRANSFERS
```

## ORGANISATIONS

Represents a school, association, public administration, company, NGO, university, cultural entity or other institutional organisation.

Primary key: `organisation_id`.

An organisation is created once and can participate in multiple projects and relationships.

## ORGANISATION_IDENTIFIERS

Stores official or source-specific organisation identifiers separately from the internal P4CRM ID.

Typical use: an official educational-centre code.

Important fields: `organisation_id`, `scheme`, `value`, `source_id`, `is_primary`.

## CONTACT_POINTS

Represents an email, phone, URL or postal address associated with an organisation or optional named professional.

Primary key: `contact_point_id`.

An address existing here does **not** imply permission for recurring communication.

Email duplicate comparison is performed on a canonical normalised value while preserving a display value operationally.

## CONTACT_POINT_SOURCES

Keeps provenance history when the same contact point is observed again in a source.

Important fields: `contact_point_id`, `source_id`, `first_seen_at`, `last_seen_at`, `source_reference`.

A re-import should update provenance rather than erase previous source history.

## PEOPLE

Optional professional-person records. P4CRM should avoid creating a named-person record when a generic institutional contact is sufficient.

## SOURCES

Records where imported/contact data came from and when it was checked.

Important fields include `source_type`, `source_name`, `source_url`, `publisher`, `retrieved_at` and `licence_or_terms`.

## IMPORT_BATCHES

Audit record for an import execution.

Important fields include `source_id`, `imported_at`, `importer_version`, `source_snapshot_ref`, `row_count`, `accepted_count`, `rejected_count` and `status`.

## PROSPECTS

Represents a potential relationship between an organisation and a P4CRM project/programme. This is not a consent table.

A school can be a PROYECT4 prospect even when all related consent scopes remain absent or `NOT_GRANTED`.

## CONSENT_REQUESTS

Represents a request to confirm one or more communication purposes. A request is not consent.

Important fields include:

- `contact_point_id`
- `organisation_id`
- `origin_interaction_id`
- `sender_controller_code`
- `target_controller_code`
- `destination`
- `status`
- `token_hash`
- `created_at`, `sent_at`, `expires_at`, `confirmed_at`
- form/text/privacy versions
- evidence reference

Only a digest of the confirmation token is stored.

## CONSENT_REQUEST_SCOPES

Lists the purposes offered in a confirmation request and the resulting decision for each one.

Typical decisions: `PENDING`, `GRANTED`, `NOT_GRANTED`.

A confirmation cannot grant a purpose that was not offered by its request.

## CONSENTS

Represents the current consent state for a specific scope.

Natural scope:

```text
contact_point_id + controller_code + purpose_code + channel
```

Initial generic purposes:

- `P4_EDUCATIONAL_RELATION`
- `PARTNER_EDUCATIONAL_INFO`
- `PARTNER_GENERAL_UPDATES`

`PARTNER` is a deployment-configurable external controller placeholder, not the name of a fixed real-world organisation.

## CONSENT_EVENTS

Append-only history of grants, revocations, declines and expirations.

Every grant created by an email-confirmation workflow should be reconstructable from the event, request, timestamp, form/text/privacy versions and evidence metadata.

## SUPPRESSIONS

Prevents communication after an unsubscribe, objection, bounce, invalid address, manual block or complaint.

Suppressions survive later imports and must be checked when audiences are evaluated.

## INTERACTIONS

Append-oriented relationship and communication log.

Examples include phone calls, confirmation requests, confirmation emails, meetings, form submissions, enquiries, participation and other relationship activity.

## CAMPAIGNS

Defines a communication initiative, purpose and audience rule. It does not itself prove that a particular recipient is eligible.

Audience generation must evaluate current permission/legal-basis and suppression state at send time.

## DATA_TRANSFERS

Audit record for authorised communication of data from one controller to another.

Important fields include `from_controller_code`, `to_controller_code`, `purpose_code`, `legal_basis`, `consent_id`, `transferred_at` and `status`.

For a generic partner flow, a completed transfer follows:

```text
valid PARTNER consent
      |
      v
DATA_TRANSFER: P4 -> PARTNER
```

The transfer references the consent that authorised the relevant purpose.

## PROJECTS

Registry of CRM-relevant initiatives and collaborations.

Generic initial codes include:

- `P4` — PROYECT4 institutional relationship
- `PARTNER` — configurable external partner relationship
- additional deployment/project codes as required

A project code must not be used to guess the legal identity of a controller.

## OPPORTUNITIES

Tracks substantive future collaboration with an organisation, for example educational projects, sustainability programmes, escape rooms, heritage, entrepreneurship, coexistence/social-relations work or case-based learning.

## Data rules for v0.2

- Stable IDs are not recycled.
- Official identifiers are preferred for deterministic organisation matching when available.
- Ambiguous organisation matches are reviewed instead of force-merged.
- Importing or re-observing an address does not create consent.
- A confirmation request does not create consent.
- Raw confirmation tokens are not stored.
- Consent is not inherited between controllers or purposes.
- Interests do not imply permission.
- Suppressions survive re-imports.
- A completed third-party transfer points back to its authorising consent.
- Real operational contact data and consent evidence must not be committed to GitHub.
