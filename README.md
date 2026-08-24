# P4CRM

**P4CRM** is an open-source CRM for institutional contacts, consent, educational outreach and long-term project relationships.

Developed by **PROYECT4 — Asociación Canaria para el Desarrollo Integral de las Personas y el Territorio**.

## Purpose

P4CRM manages relationships with organisations and professional contacts while keeping data provenance, communication permissions, interactions and authorised transfers traceable.

It is intended for relationships with schools, AMPAs, education professionals, associations, NGOs, public/private institutions, companies, partners and organisations interested in educational, environmental, cultural, social or entrepreneurial initiatives.

P4CRM is not just a sales database. Its core objects are **relationships, permissions, communication workflows and project opportunities**.

## Core principles

### Contact is not consent

A professional or institutional contact may exist with documented provenance without being authorised for recurring promotional/marketing email.

### Consent is scoped

Where consent is the applicable basis, P4CRM models it by:

```text
contact point + controller + purpose + channel
```

### Requests are not grants

A phone call may initiate an email-confirmation request. The request remains separate from consent until the recipient performs the required affirmative confirmation action.

### Traceability

P4CRM preserves source provenance, import batches, consent events, suppression history, interactions and authorised transfers.

### Suppressions survive imports

An unsubscribe, objection or block is not removed merely because the same address is later found again in a directory.

### Open source, private operational data

Code, architecture and schemas are open. Real CRM records, consent evidence, raw confirmation tokens and credentials are not committed to this repository.

## v0.2

Schema v0.2 adds repeatable imports and phone-to-email consent confirmation.

Current entities:

```text
ORGANISATIONS
ORGANISATION_IDENTIFIERS
CONTACT_POINTS
CONTACT_POINT_SOURCES
PEOPLE
SOURCES
IMPORT_BATCHES
PROSPECTS
CONSENTS
CONSENT_EVENTS
CONSENT_REQUESTS
CONSENT_REQUEST_SCOPES
SUPPRESSIONS
INTERACTIONS
CAMPAIGNS
DATA_TRANSFERS
PROJECTS
OPPORTUNITIES
```

The machine-readable contract is [schemas/p4crm-v0.2.json](schemas/p4crm-v0.2.json). v0.1 remains available as the previous versioned contract.

## Institutional import flow

```text
official / professional source
          |
          v
     normalisation
          |
          +--> SOURCES / IMPORT_BATCHES
          +--> ORGANISATIONS
          +--> ORGANISATION_IDENTIFIERS
          +--> CONTACT_POINTS
          +--> CONTACT_POINT_SOURCES
          +--> PROSPECTS
```

The v0.2 importer uses deterministic IDs so repeated imports can resolve the same organisation/contact instead of creating a new record every time.

An imported address does **not** generate consent.

See [Import contract](docs/import-contract.md).

## Phone -> email confirmation

An organisation can provide an address during a phone call and request a confirmation message.

```text
PHONE_CALL
    |
    v
CONSENT_REQUEST
    |
    v
neutral confirmation email
(one-time opaque token)
    |
    v
confirmation/preferences page
    |
    v
explicit affirmative action
    |
    +--> CONSENT
    +--> append-only CONSENT_EVENT
```

The raw token is not persisted: P4CRM stores only a cryptographic digest. Requests expire and are single-use.

See [Email confirmation after a phone call](docs/email-confirmation-flow.md) and [Consent and transfer flow](docs/consent-flow.md).

## Initial purposes

### PROYECT4

`P4_EDUCATIONAL_RELATION`

Educational resources, activities, initiatives and projects from PROYECT4 within the scope explained to the recipient.

### Partner organisation

`PARTNER_EDUCATIONAL_INFO`

Educational materials/resources, educational visits and educational activities offered by an external partner.

`PARTNER_GENERAL_UPDATES`

Separately selectable general updates from that partner.

The v0.1 generic code `PARTNER_EDUCATIONAL_VISITS` is deprecated and maps to `PARTNER_EDUCATIONAL_INFO`.

The exact legal entity represented by the `PARTNER` controller code **must be configured and verified for each deployment before production use**. See [config/controller-registry.example.json](config/controller-registry.example.json).

## Partner transfer boundary

P4CRM belongs to PROYECT4. A partner is represented as a configurable external project/controller.

Where PROYECT4 collects a valid authorisation for a partner purpose, P4CRM may record the later transfer:

```text
confirmed PARTNER consent
          |
          v
DATA_TRANSFER: P4 -> PARTNER
          |
          v
only data required for the granted purpose
```

Every completed transfer points back to the consent that authorised it.

## Reference implementation

The v0.2 repository contains storage-agnostic Python helpers using only the standard library:

- `src/p4crm/importer.py` — email/URL normalisation and deterministic IDs;
- `src/p4crm/confirmation.py` — one-time confirmation request/token domain flow;
- `scripts/prepare_import.py` — CSV staging into accepted/rejected JSONL;
- `scripts/validate_contract.py` — repository/schema validation;
- `tests/` — contract, importer and confirmation tests.

These helpers do not select the final production database or email provider.

## Repository structure

```text
P4CRM/
├── .github/workflows/
├── config/
├── docs/
├── schemas/
├── scripts/
├── src/p4crm/
├── tests/
├── CHANGELOG.md
└── README.md
```

## Google Drive prototype

The current operational prototype uses the shared P4CRM Google Drive workspace and the `P4CRM_CORE` Google Sheet. GitHub is the source of truth for code, schemas, tests and technical documentation; operational CRM data stays outside the public repository.

## Privacy and data protection

P4CRM is designed around purpose limitation, data minimisation, scoped permissions, evidence, withdrawal, suppression, provenance and controller separation.

The schema supports compliance work but does not itself determine the lawful basis of any specific communication. Each deployment and campaign must apply the relevant data-protection and electronic-communications rules.

## Project status

**v0.2 — import + email-confirmation foundation. Early development.**

The public educational-resources website remains a separate project. It may later send consent/interaction events into P4CRM through a defined integration.

## Roadmap

1. Connect the v0.2 import staging layer to the operational CRM store.
2. Import and review the first controlled educational-centre dataset.
3. Implement suppression-aware audience selection.
4. Implement the confirmation endpoint and mail-provider adapter.
5. Configure and verify deployment-specific partner controllers.
6. Implement authorised partner export/transfer.
7. Add campaign delivery and interaction ingestion.
8. Add project/opportunity workflows.
9. Define user roles, access control and retention policies.

## License

A suitable open-source licence will be selected before the first stable release.

---

**P4CRM**  
PROYECT4 — Asociación Canaria para el Desarrollo Integral de las Personas y el Territorio
