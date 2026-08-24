# Changelog

All notable changes to P4CRM will be documented here.

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
