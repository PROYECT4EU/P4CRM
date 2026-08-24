# P4CRM architecture — v0.1

## Scope

P4CRM is the institutional relationship and marketing CRM of **PROYECT4 — Asociación Canaria para el Desarrollo Integral de las Personas y el Territorio**.

The CRM is deliberately separate from the public educational-resources website. The website may later act as a data-acquisition and consent interface, while P4CRM remains the system of record for contacts, relationships, permissions and communication history.

## System boundaries

```text
PUBLIC / PROFESSIONAL SOURCES
            |
            v
          P4CRM
  organisations + contacts
            |
            +--> PROYECT4 relationship
            |
            +--> consent records
            |
            +--> campaigns / interactions
            |
            +--> opportunities / projects
            |
            +--> authorised data transfers
                         |
                         v
              SAN BLAS RESERVA AMBIENTAL
              only when specifically authorised
```

### In scope

- Organisations and professional contacts
- Contact-point provenance
- Institutional relationship tracking
- Segmentation and interests
- Consent evidence and consent history
- Suppression / do-not-contact controls
- Campaign definitions and interaction history
- Project and opportunity tracking
- Traceability of authorised transfers to third parties
- Analytics derived from CRM activity

### Out of scope for v0.1

- The public educational-resources website itself
- Bulk email delivery infrastructure
- Authentication and role-based access control implementation
- A production database backend
- Automated synchronisation with San Blas systems
- Automated scraping or uncontrolled ingestion of contact data

## Data ownership and responsibility

P4CRM is operated for PROYECT4. A record existing in P4CRM does **not** imply consent to receive marketing communication.

A contact may have several independent relationships and permissions. Consent must therefore be represented by:

```text
contact point + controller + purpose + channel + status
```

rather than by a single global `marketing_allowed` flag.

## San Blas flow

The initial design supports the following workflow:

1. PROYECT4 records an organisation and a professional/institutional contact point with its source.
2. The contact may receive or discover educational resources through a legally appropriate route.
3. A PROYECT4 consent may be collected for PROYECT4 educational communications.
4. Separately, the contact may explicitly authorise PROYECT4 to communicate its email address to the legal entity responsible for San Blas Reserva Ambiental for information about educational visits and activities.
5. Only after that specific authorisation may a `DATA_TRANSFERS` record be created.
6. Withdrawal from San Blas communications must not automatically withdraw consent for PROYECT4, and vice versa.

The final legal identity of the San Blas data controller must be configured before production use.

## Google Drive operational layer

The initial operational workspace is the shared Drive `P4CRM`:

```text
P4CRM/
├── 00_ADMIN/
├── 01_DATA/
├── 02_MARKETING/
├── 03_RESOURCES/
├── 04_WEB/
└── 05_ANALYTICS/
```

`01_DATA/P4CRM_CORE` currently mirrors the v0.1 logical model for prototyping and data preparation.

## GitHub source-of-truth layer

This repository is the source of truth for:

- schema definitions;
- enum definitions;
- technical documentation;
- import/export logic;
- application code;
- tests;
- migrations.

Operational contact data and consent evidence must not be committed to the public repository.

## Design principles

1. **One organisation, many relationships.** Do not duplicate an organisation for every project.
2. **Contact point is not consent.** A public professional email can be stored with provenance without becoming an authorised marketing contact.
3. **Consent is scoped.** Controller, purpose and channel are mandatory dimensions.
4. **Suppressions survive imports.** Opt-outs must prevent accidental reactivation after a later directory import.
5. **Every imported datum has provenance.** Source and verification date are first-class data.
6. **Transfers are explicit events.** Sharing an authorised contact with another controller is separately traceable.
7. **Interests are not permissions.** Segmentation and inferred/reported interests never replace consent or another applicable legal basis.
8. **No personal data in Git.** Production data belongs in controlled operational storage, not this repository.

## Versioning

This document describes **schema v0.1**. Breaking changes to entity meaning or required relationships should increment the schema version and be accompanied by a migration note.
