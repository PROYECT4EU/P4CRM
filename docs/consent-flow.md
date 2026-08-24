# Consent and transfer flow — v0.1

## Principle

P4CRM does not use a single global marketing flag. Permissions are scoped by:

```text
contact point + controller + purpose + channel
```

A contact may therefore authorise PROYECT4 educational communication and independently accept or refuse communication of the same contact point to the entity responsible for San Blas Reserva Ambiental.

## Initial states

A professional or institutional email imported from a public/professional source may exist as:

```text
CONTACT_POINT.status = ACTIVE
PROSPECT.relationship_status = NEW
CONSENT = absent or NOT_GRANTED
```

This state means that the contact exists in the relationship database. It does not by itself mean that a marketing campaign is authorised.

## PROYECT4 consent

Initial purpose code:

```text
controller_code = P4
purpose_code    = P4_EDUCATIONAL_RELATION
channel         = EMAIL
```

This purpose is intended for PROYECT4 information about educational resources, activities, initiatives and projects within the scope presented to the subscriber.

## San Blas consent / authorisation

Initial purpose code:

```text
controller_code = SAN_BLAS
purpose_code    = SAN_BLAS_EDUCATIONAL_VISITS
channel         = EMAIL
```

This permission must be presented separately from the PROYECT4 permission.

Before production use, `SAN_BLAS` must resolve to the exact legal entity that will act as recipient/controller for the subsequent communication.

## Expected form behaviour

Conceptually the public form should allow four outcomes:

```text
P4 = NO   | SAN_BLAS = NO
P4 = YES  | SAN_BLAS = NO
P4 = NO   | SAN_BLAS = YES
P4 = YES  | SAN_BLAS = YES
```

Access to free educational resources should not depend on selecting either optional communication permission.

## Evidence

For each consent event, preserve enough evidence to reconstruct what happened:

- `contact_point_id`
- controller
- purpose
- channel
- status
- timestamp
- collection source
- form identifier
- consent-text version
- privacy-notice version
- evidence reference when available

The application layer should prefer an append-only consent-event history. The v0.1 Sheet prototype currently represents the logical state and evidence fields; a later implementation may split current state from immutable events.

## Transfer to San Blas

A completed transfer should follow this chain:

```text
CONTACT_POINT
     |
     v
CONSENT: SAN_BLAS_EDUCATIONAL_VISITS = GRANTED
     |
     v
DATA_TRANSFER: P4 -> SAN_BLAS
     |
     v
San Blas receives only the authorised data required for that purpose
```

A `DATA_TRANSFERS` row should contain the `consent_id` that authorised the transfer.

## Withdrawal and suppression

Withdrawal is scoped. Examples:

```text
P4 educational email       = GRANTED
San Blas educational email = REVOKED
```

or the inverse are both valid states.

A withdrawal or objection should also generate/maintain the appropriate suppression state so that a later directory import cannot silently reactivate the contact.

## Send-time rule

Future campaign tooling should evaluate eligibility at send time, not only when a list is created.

Conceptually:

```text
eligible =
  contact point is active
  AND required permission/legal basis is valid
  AND no matching suppression exists
  AND campaign purpose matches the permission scope
```

The exact legal basis and operational rule for each campaign remains deployment-specific and must not be inferred solely from the presence of a contact record.
