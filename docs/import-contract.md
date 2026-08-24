# Import contract — v0.1

This contract defines how external professional/institutional sources should enter P4CRM before any production importer is implemented.

## Goal

Import source data without confusing **discoverability** with **permission to communicate**.

An imported institutional email should normally create or update:

```text
SOURCES
ORGANISATIONS
CONTACT_POINTS
PROSPECTS
```

It should **not** create a `GRANTED` consent unless the import itself is evidence of an already valid, documented consent event.

## Minimum source record

Every import batch must identify:

| Field | Required | Example |
|---|---:|---|
| `source_type` | yes | `PUBLIC_DIRECTORY` |
| `source_name` | yes | Name of official directory |
| `source_url` | when available | Canonical source URL |
| `publisher` | when available | Publishing institution |
| `retrieved_at` | yes | ISO timestamp |
| `notes` | no | Scope/version notes |

## Minimum organisation record

For the initial educational-centre use case:

| Field | Required |
|---|---:|
| `name` | yes |
| `organisation_type` | yes |
| `country` | recommended |
| `region` | recommended |
| `island` | recommended |
| `municipality` | recommended |
| `website` | when available |

Do not create duplicate organisations merely because the same centre appears in several source directories.

## Minimum contact-point record

| Field | Required |
|---|---:|
| `organisation_id` | yes |
| `contact_type` | yes |
| `value` | yes |
| `is_generic` | yes |
| `source_id` | yes |
| `verified_at` | recommended |
| `status` | yes |

For email addresses, normalisation should trim whitespace and compare values case-insensitively for duplicate detection while preserving a canonical display value.

## Prospect creation

The initial education-directory import may create a PROYECT4 prospect such as:

```text
project_code        = P4
relationship_status = NEW
segment             = EDUCATION
```

Additional segmentation such as island, municipality, educational stage or organisation type should be derived from organisation/source metadata where available rather than embedded into consent state.

## Suppression check

Before a new or re-imported contact point can be considered for any outreach workflow, the importer or downstream audience builder must check existing suppressions.

A suppression must not be deleted or ignored because the same email was discovered again in a newer source.

## Duplicate strategy

Prefer deterministic review rules:

1. Match exact normalised contact point.
2. Reuse its existing organisation where appropriate.
3. If organisation identity is uncertain, flag for review rather than auto-merging unrelated entities.
4. Keep multiple `SOURCES`/verification events when useful for provenance.

## Import errors

Rows should be rejected or quarantined when:

- the organisation cannot be identified;
- a contact value is malformed;
- source provenance is missing;
- required enum values are unknown;
- an attempted import tries to set consent to `GRANTED` without valid evidence metadata.

## Data not allowed in the public repository

Import files containing real contact details, named-person data or consent evidence must remain in controlled operational storage and are excluded by `.gitignore` patterns. Synthetic fixtures may be used in tests.
