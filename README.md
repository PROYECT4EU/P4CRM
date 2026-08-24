# P4CRM

**P4CRM** is an open-source CRM for managing institutional contacts, communication consent, segmentation, educational outreach and long-term project relationships.

The project is developed by **PROYECT4 — Asociación Canaria para el Desarrollo Integral de las Personas y el Territorio**.

## Purpose

P4CRM provides a simple and transparent way to manage relationships with organisations and professional contacts while keeping provenance, permissions, communication history and data use traceable.

The system is intended for relationships with:

- schools and educational centres;
- teachers and education professionals;
- associations and NGOs;
- public and private institutions;
- companies and professional contacts;
- project partners and collaborators;
- organisations interested in educational, environmental, cultural, social or entrepreneurial initiatives.

P4CRM is not intended to be just a sales database. Its main purpose is to manage **relationships, permissions, communication workflows and project opportunities**.

## Core principles

### Contact is not consent

A professional or institutional contact can exist in P4CRM with documented provenance without being authorised for marketing communication.

### Consent is scoped

Where consent is the applicable basis, P4CRM models it by:

```text
contact point + controller + purpose + channel
```

Consent must not be assumed to apply automatically to another organisation, project or purpose.

### Data minimisation

Only information useful for a legitimate relationship or communication purpose should be stored.

### Traceability

P4CRM records the source of imported contact data and is designed to keep consent, suppression, interaction and transfer history auditable.

### Separation of purposes

A school may independently:

- receive educational information from PROYECT4;
- participate in a PROYECT4 educational project;
- be interested in sustainability workshops or escape rooms;
- authorise its contact details to be communicated for information about educational visits to Reserva Ambiental San Blas.

Those relationships and permissions remain distinguishable.

### Suppressions survive imports

An unsubscribe, objection or block must not disappear simply because the same address is later found again in a public directory.

### Open source, private operational data

The code, architecture and schema are open. Real CRM contact records, consent evidence and credentials are **not** stored in this public repository.

## v0.1 foundation

The first implementation milestone establishes the CRM data contract and workflows before the production runtime is selected.

Current v0.1 entities:

```text
ORGANISATIONS
CONTACT_POINTS
PEOPLE
SOURCES
PROSPECTS
CONSENTS
SUPPRESSIONS
INTERACTIONS
CAMPAIGNS
DATA_TRANSFERS
PROJECTS
OPPORTUNITIES
```

Documentation:

- [Architecture](docs/architecture.md)
- [Data model](docs/data-model.md)
- [Consent and transfer flow](docs/consent-flow.md)
- [Machine-readable v0.1 table contract](schemas/p4crm-v0.1.json)
- [Controlled values](config/enums.json)
- [Changelog](CHANGELOG.md)

## Initial San Blas use case

P4CRM belongs to PROYECT4. Reserva Ambiental San Blas is represented as a related external project/use case.

The intended flow is:

```text
professional / institutional source
              |
              v
            P4CRM
              |
      PROYECT4 relationship
              |
              +--> optional PROYECT4 educational consent
              |
              +--> separate San Blas authorisation
                          |
                          v
                authorised data transfer
                          |
                          v
              Reserva Ambiental San Blas
```

Only contacts that have the required specific authorisation may be included in the corresponding San Blas transfer workflow.

The exact legal entity behind the `SAN_BLAS` controller code must be confirmed before production use.

## Educational relationships

P4CRM supports long-term institutional relationships instead of treating every contact as a sales lead.

Potential future PROYECT4 work with an organisation may include:

- sustainability and environmental education;
- biodiversity, territory and heritage;
- entrepreneurship;
- social relationships and coexistence;
- educational escape rooms;
- case-based learning;
- arts and creative education;
- new educational resources and activities.

These interests may be used for relationship management and segmentation, but **interests are not permissions**.

## Repository structure

```text
P4CRM/
├── config/       # controlled values and configuration contracts
├── docs/         # architecture and workflow documentation
├── schemas/      # versioned data contracts
├── scripts/      # future import/export/migration tooling
├── src/          # future application source
├── tests/        # contract and workflow tests
├── CHANGELOG.md
└── README.md
```

Operational data is maintained outside the public Git repository.

## Planned capabilities

### Contact and organisation management

- organisations;
- optional named professional contacts;
- multiple contact points per organisation;
- source provenance and verification dates;
- tags, interests and segmentation;
- relationship history.

### Consent and suppression management

- scoped consent records;
- consent source and timestamp;
- wording and privacy-notice versions;
- communication channels and purposes;
- withdrawal history;
- suppression lists;
- evidence references.

### Communication management

- campaign definitions;
- audience rules;
- communication history;
- frequency controls;
- unsubscribe/suppression enforcement;
- future delivery-system integration.

### Projects and opportunities

- project registry;
- relationship opportunities;
- educational project themes;
- follow-up stages;
- participation and collaboration history.

### Authorised transfers

P4CRM can record an explicit transfer event when a contact has authorised data communication to another controller for a defined purpose. The transfer record points back to the authorising consent/evidence.

## Google Drive prototype

The current operational prototype uses a shared Google Drive workspace and a `P4CRM_CORE` Google Sheet that mirrors the v0.1 logical model for early data preparation.

GitHub remains the source of truth for schema, code, scripts, tests and technical documentation. Google Drive contains operational working data and must not be treated as a public-code repository.

## Privacy and data protection

P4CRM is intended to be designed around privacy by default, including:

- purpose limitation;
- data minimisation;
- scoped permissions where applicable;
- consent evidence;
- withdrawal management;
- access control;
- retention policies;
- export/deletion workflows;
- suppression of contacts who opt out;
- separation between controllers and communication purposes.

Compliance with applicable data-protection and electronic-communications rules must be evaluated according to each deployment and use case. P4CRM's schema does not itself determine the lawful basis of a particular communication.

## Project status

**Schema / architecture v0.1 — early development.**

The public educational-resources website is being treated as a separate project. P4CRM may later receive consent and interaction events from that website through a defined integration.

## Roadmap

1. Finalise and validate schema v0.1.
2. Define stable ID generation and normalisation rules.
3. Implement source/import validation.
4. Import the first controlled set of educational organisations.
5. Implement suppression-aware audience logic.
6. Implement consent-event history.
7. Implement San Blas authorised-transfer export.
8. Add campaign and interaction tooling.
9. Add project/opportunity workflows.
10. Define user roles, access control and production storage.

## Contributing

P4CRM is intended to evolve as an open-source project. Contribution guidelines will be added as the project structure becomes stable.

## License

A suitable open-source licence will be selected before the first stable release.

---

**P4CRM**  
PROYECT4 — Asociación Canaria para el Desarrollo Integral de las Personas y el Territorio
