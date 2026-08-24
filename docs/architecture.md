# P4CRM architecture — v0.2

## Scope

P4CRM is the institutional relationship and marketing CRM of **PROYECT4 — Asociación Canaria para el Desarrollo Integral de las Personas y el Territorio**.

The CRM is deliberately separate from any public educational-resources website. A website may act as a data-acquisition and consent interface, while P4CRM remains the system of record for contacts, relationships, permissions and communication history.

## System boundaries

```text
PUBLIC / PROFESSIONAL SOURCES
            |
            v
          P4CRM
  organisations + contacts
            |
            +--> PROYECT4 relationship
            +--> consent requests / confirmations
            +--> consent + suppression records
            +--> campaigns / interactions
            +--> opportunities / projects
            +--> authorised data transfers
                         |
                         v
                    PARTNER
              only when authorised
```

`PARTNER` is a configurable external controller/project placeholder. The public repository does not encode the identity of any deployment-specific partner.

## In scope

- Organisations and professional contacts
- Contact-point provenance and repeat-import history
- Institutional relationship tracking
- Segmentation and interests
- Consent requests, confirmation, evidence and event history
- Suppression / do-not-contact controls
- Campaign definitions and interaction history
- Project and opportunity tracking
- Traceability of authorised transfers to third parties
- Analytics derived from CRM activity

## Out of scope for v0.2

- Public educational-resource websites themselves
- Final bulk-email delivery infrastructure
- Authentication and role-based access control implementation
- Final production database backend
- Deployment-specific partner-system integrations
- Automated scraping or uncontrolled ingestion of contact data

## Data ownership and responsibility

P4CRM is operated for PROYECT4. A record existing in P4CRM does **not** imply consent to receive marketing communication.

A contact may have several independent relationships and permissions. Consent is represented by:

```text
contact point + controller + purpose + channel + status
```

rather than by a single global `marketing_allowed` flag.

## Partner flow

The generic external-partner workflow is:

1. PROYECT4 records an organisation and professional/institutional contact point with provenance.
2. A phone call or another valid interaction may create a confirmation request.
3. The confirmation request is not itself a grant of email consent.
4. The recipient may affirm one or more explicitly offered partner purposes.
5. The resulting `CONSENTS` current state and append-only `CONSENT_EVENTS` are stored separately.
6. Only after the required authorisation may a `DATA_TRANSFERS` record be completed for that partner and purpose.
7. Withdrawal from partner communications does not automatically withdraw an independent PROYECT4 permission, and vice versa.

The exact legal identity and privacy information for a deployment's `PARTNER` must be configured before production use.

## Import architecture

v0.2 adds repeatable import identity and provenance:

```text
SOURCES
  |----< IMPORT_BATCHES
  |----< CONTACT_POINT_SOURCES

ORGANISATIONS
  |----< ORGANISATION_IDENTIFIERS
  |----< CONTACT_POINTS
  |----< PROSPECTS
```

Official identifiers are preferred when available. Ambiguous identity matches are reviewed rather than force-merged.

## Confirmation architecture

```text
INTERACTION: PHONE_CALL
        |
        v
CONSENT_REQUESTS
        |----< CONSENT_REQUEST_SCOPES
        |
        v
one-time email token
        |
        v
explicit confirmation
        |
        +----> CONSENTS (current state)
        +----> CONSENT_EVENTS (append-only history)
```

Raw confirmation tokens are never persisted; only cryptographic digests are stored.

## Google Drive operational layer

The initial operational workspace is the shared Drive `P4CRM`, with `P4CRM_CORE` mirroring the current logical model for prototyping and data preparation.

## GitHub source-of-truth layer

This repository is the source of truth for schema definitions, enum definitions, technical documentation, import/export logic, application code, tests and migrations.

Operational contact data and consent evidence must not be committed to the public repository.

## Design principles

1. **One organisation, many relationships.** Do not duplicate an organisation for every project.
2. **Contact point is not consent.** A public professional email can exist with provenance without becoming an authorised marketing contact.
3. **Consent is scoped.** Controller, purpose and channel are mandatory dimensions.
4. **Requests are not grants.** Confirmation workflows preserve the distinction between a request and an affirmative consent event.
5. **Suppressions survive imports.** Opt-outs prevent accidental reactivation after later directory imports.
6. **Every imported datum has provenance.** Source and verification history are first-class data.
7. **Transfers are explicit events.** Sharing an authorised contact with another controller is separately traceable.
8. **Interests are not permissions.** Segmentation never replaces consent or another applicable legal basis.
9. **Partner identity is deployment configuration.** Public code uses `PARTNER`; real controller identities belong in deployment-specific configuration.
10. **No operational personal data in Git.** Production data belongs in controlled storage, not this repository.

## Versioning

This document describes **schema v0.2**. Breaking changes to entity meaning or required relationships should increment the schema version and be accompanied by a migration note.
