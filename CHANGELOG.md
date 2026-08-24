# Changelog

All notable changes to P4CRM will be documented here.

## [0.2] - 2026-08-24

### Added

- Deterministic institutional/professional import normalisation.
- Stable organisation, contact-point and prospect identifiers for repeat imports.
- `ORGANISATION_IDENTIFIERS` for official/source identifiers such as educational-centre codes.
- `CONTACT_POINT_SOURCES` to preserve provenance across re-observations.
- `IMPORT_BATCHES` contract for auditable imports and rejection counts.
- `CONSENT_REQUESTS` and `CONSENT_REQUEST_SCOPES` for consent-confirmation workflows.
- Append-only `CONSENT_EVENTS` audit model alongside current consent state.
- Phone-call to email-confirmation workflow with one-time, expiring tokens.
- Storage-agnostic confirmation implementation using cryptographically random tokens and stored SHA-256 digests.
- Separate San Blas scopes for educational information and general updates.
- Staging CSV import preparation script with accepted/rejected JSONL output.
- Tests covering import identity, provenance and consent-confirmation security/state transitions.
- Example controller registry that blocks San Blas production readiness until its exact legal entity is verified.

### Changed

- `SAN_BLAS_EDUCATIONAL_VISITS` is deprecated in favour of `SAN_BLAS_EDUCATIONAL_INFO`, covering educational materials/resources, visits and educational activities.
- General San Blas updates are a separate `SAN_BLAS_GENERAL_UPDATES` purpose.
- The repository contract validator now targets schema v0.2.

### Security / privacy

- A telephone request for a confirmation email does not itself create a `GRANTED` email consent in this workflow.
- Raw confirmation tokens must not be stored or logged; only their digest is persisted.
- Confirmation requests are time-limited and single-use.
- Only purpose scopes offered in a request can be granted by that request.

### Notes

- The exact legal identity represented by `SAN_BLAS` remains a production blocker and is not invented by the project.
- v0.2 still separates open-source code/schema from real operational contact and consent data.

## [0.1] - 2026-08-24

### Added

- Initial P4CRM architecture definition.
- Logical data model for organisations, contact points, people and sources.
- Prospect and institutional-relationship model.
- Scoped consent model based on contact point, controller, purpose and channel.
- Suppression model to preserve opt-outs across later imports.
- Campaign and interaction entities.
- Project and opportunity tracking for long-term educational relationships.
- Explicit data-transfer audit model for authorised transfers from PROYECT4 to third parties.
- Initial San Blas educational-visits consent flow.
- Machine-readable v0.1 table contract and controlled enums.
- Repository rules preventing operational CRM exports and credentials from being committed.

### Notes

- v0.1 is a schema/architecture baseline, not a production release.
- The legal identity behind the `SAN_BLAS` controller code remains intentionally unresolved until confirmed.
- The public educational-resources website is a separate project and is not implemented in this repository.
