# P4CRM

**P4CRM** is an open-source CRM for managing institutional contacts, communication consent, segmentation, and educational outreach.

The project is developed by **PROYECT4 — Asociación Canaria para el Desarrollo Integral de las Personas y el Territorio**.

## Purpose

P4CRM is designed to provide a simple and transparent way to manage relationships with organisations and professional contacts while keeping consent, communication history, and data usage traceable.

The system is intended for relationships with:

* Schools and educational centres
* Teachers and education professionals
* Associations and NGOs
* Public and private institutions
* Companies and professional contacts
* Project partners and collaborators
* Organisations interested in educational, environmental, cultural, social or entrepreneurial initiatives

P4CRM is not intended to be just a sales database. Its main purpose is to manage **relationships, permissions and communication workflows**.

## Core principles

### Consent first

Every communication should be linked to a clear legal basis and, where consent is used, to a traceable consent record.

P4CRM should make it possible to record:

* Who gave consent
* When consent was given
* How it was collected
* What information was provided at the time
* What types of communication were authorised
* Which organisation or project may use the data
* Consent status
* Withdrawal or modification of consent

Consent should never be assumed to apply automatically to another organisation, project or purpose.

### Data minimisation

Only information that is useful for a legitimate relationship or communication purpose should be stored.

### Traceability

Changes to consent, contact information and communication preferences should be auditable.

### Separation of purposes

A contact may have different relationships with different projects.

For example, a school may:

* Receive educational resources from PROYECT4
* Request information about future educational projects
* Be interested in sustainability workshops or escape rooms
* Request information about visits to Reserva Ambiental San Blas

P4CRM should keep those purposes and permissions distinguishable.

### Open source

P4CRM is being developed as an open project so that its architecture and data-processing logic can be inspected, improved and reused.

## Planned capabilities

P4CRM is expected to include:

### Contact management

* Organisations
* Individual professional contacts
* Contact roles
* Multiple contacts per organisation
* Contact sources
* Tags and segmentation
* Notes and relationship history

### Consent management

* Consent records
* Consent source
* Consent timestamp
* Consent wording/version
* Communication channels
* Authorised purposes
* Data controller or authorised organisation
* Consent withdrawal
* Suppression lists
* Consent history

### Organisations and projects

Contacts may be associated with one or more projects while maintaining separate communication permissions.

Initial use cases include:

**PROYECT4**

Educational and institutional communication related to projects involving areas such as:

* Sustainability
* Environmental education
* Local history and heritage
* Entrepreneurship
* Social relationships
* Educational escape rooms
* Case-based learning
* Educational resources and activities

**Reserva Ambiental San Blas**

Contacts that have the appropriate permission may also be managed for communications related to educational visits and activities at Reserva Ambiental San Blas.

The CRM must preserve the distinction between the original PROYECT4 relationship and any additional purpose or organisation authorised by the contact.

### Communication management

Planned functionality may include:

* Contact lists
* Segmentation
* Campaign audiences
* Communication history
* Email templates
* Campaign tracking
* Exclusion lists
* Frequency controls
* Unsubscribe management

### Educational relationships

The CRM should also support long-term institutional relationships rather than treating every contact as a sales lead.

Examples include:

* Schools previously contacted
* Schools that have participated in activities
* Teachers interested in resources
* Potential educational partners
* Institutions interested in future projects
* Project proposals and follow-up
* Historical participation

## Data model

The initial model is expected to distinguish at least between:

```text
Organisation
    └── Contact
          ├── Relationship
          ├── Consent
          ├── Communication preferences
          ├── Tags / Segments
          └── Interaction history

Project
    ├── Purpose
    └── Authorised contacts

Campaign
    ├── Audience
    ├── Purpose
    └── Communication history
```

The exact technical implementation is still under development.

## Privacy and data protection

P4CRM is intended to be designed around privacy by default.

Important design requirements include:

* Purpose limitation
* Data minimisation
* Explicit consent scopes where applicable
* Consent evidence
* Withdrawal management
* Access control
* Retention policies
* Export and deletion workflows
* Suppression of contacts who opt out
* Separation between organisations and communication purposes

Compliance with applicable data-protection and electronic-communications rules must be evaluated according to each deployment and use case.

## Project status

**Early development.**

The repository is currently being structured and the initial CRM architecture, data model and workflows are being defined.

## Roadmap

Initial development priorities:

1. Define the contact and organisation data model
2. Define consent and communication-purpose models
3. Create consent history and auditability
4. Implement segmentation
5. Implement communication lists and suppression rules
6. Add campaign management
7. Add organisation and project relationship tracking
8. Add import/export tools
9. Define user roles and permissions
10. Document privacy and retention workflows

## Contributing

P4CRM is intended to evolve as an open-source project.

Contribution guidelines will be added as the project structure becomes stable.

## License

A suitable open-source licence will be selected before the first stable release.

---

**P4CRM**
PROYECT4 — Asociación Canaria para el Desarrollo Integral de las Personas y el Territorio
