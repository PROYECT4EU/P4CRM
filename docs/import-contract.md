# Import contract — v0.2

This contract defines how external professional/institutional sources enter P4CRM.

## Goal

Import source data without confusing **discoverability** with **permission to communicate** and without creating duplicate organisations on later imports.

An imported institutional email normally creates or updates:

```text
SOURCES
IMPORT_BATCHES
ORGANISATIONS
ORGANISATION_IDENTIFIERS (when an official identifier exists)
CONTACT_POINTS
CONTACT_POINT_SOURCES
PROSPECTS
```

It does **not** create a `GRANTED` consent merely because an address is public or professional.

## Stable identifiers

The importer uses deterministic identifiers so a later run over the same source does not create a fresh entity solely because the import happened on a different date.

Priority for organisation identity:

1. trusted external identifier, such as an official educational-centre code, together with its identifier scheme;
2. otherwise a conservative normalised key based on organisation name + municipality + region;
3. ambiguous matches are flagged for review rather than force-merged.

`ORGANISATION_IDENTIFIERS` keeps official/source identifiers separate from the organisation's internal P4CRM ID.

## Minimum source record

Every import batch identifies:

| Field | Required | Example |
|---|---:|---|
| `source_type` | yes | `PUBLIC_DIRECTORY` |
| `source_name` | yes | Name of official directory |
| `source_url` | when available | Canonical source URL |
| `publisher` | when available | Publishing institution |
| `retrieved_at` | yes | ISO timestamp |
| `notes` | no | Scope/version notes |

A batch also records importer version, source snapshot/reference when available, row counts and rejection counts in `IMPORT_BATCHES`.

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
| official centre/organisation identifier | strongly preferred when available |

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

For email addresses, v0.2 trims whitespace and compares the canonical lowercase address for deterministic duplicate detection.

`CONTACT_POINT_SOURCES` preserves each source in which a contact point has been observed, including `first_seen_at` and `last_seen_at`. Re-observation therefore improves provenance rather than replacing it.

## Prospect creation

The initial education-directory import creates or reuses a PROYECT4 prospect such as:

```text
project_code        = P4
relationship_status = NEW
segment             = EDUCATION
```

Additional segmentation such as island, municipality, educational stage or organisation type is derived from organisation/source metadata where available rather than embedded into consent state.

## Suppression check

Before a new or re-imported contact point can enter an outreach workflow, the importer or downstream audience builder checks existing suppressions.

A suppression is never deleted or ignored because the same email was discovered again in a newer source.

## Duplicate strategy

Use deterministic review rules:

1. Resolve an official organisation identifier when available.
2. Otherwise build the conservative organisation match key.
3. Normalise and match the contact point within that organisation.
4. Reuse existing IDs when keys match.
5. Add/update source provenance for a re-observed contact point.
6. If organisation identity is uncertain, quarantine for review rather than auto-merging unrelated entities.

## Import errors and quarantine

Rows are rejected/quarantined when:

- the organisation cannot be identified;
- a contact value is malformed;
- source provenance is missing;
- required enum values are unknown;
- an external identifier conflicts with an existing organisation;
- an attempted import tries to set consent to `GRANTED` without valid consent evidence.

Rejected rows remain operational data and must not be committed to this public repository.

## Reference implementation

`src/p4crm/importer.py` provides storage-agnostic normalisation and deterministic ID helpers for the v0.2 contract.

The next integration layer may write the resulting records to the current Google Sheet prototype or to a future database, but storage does not change these identity and provenance rules.

## Data not allowed in the public repository

Import files containing real contact details, named-person data or consent evidence remain in controlled operational storage and are excluded by `.gitignore` patterns. Synthetic fixtures may be used in tests.
