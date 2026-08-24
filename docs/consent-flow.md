# Consent and transfer flow — v0.2

## Principle

P4CRM does not use a single global marketing flag. Permissions are scoped by:

```text
contact point + controller + purpose + channel
```

A contact may therefore authorise PROYECT4 educational communication and independently accept or refuse one or more San Blas communication purposes.

## Initial states

A professional or institutional email imported from a public/professional source may exist as:

```text
CONTACT_POINT.status = ACTIVE
PROSPECT.relationship_status = NEW
CONSENT = absent or NOT_GRANTED
```

This means that the contact exists in the relationship database. It does not by itself mean that recurring email communication is authorised.

## Initial purposes

### PROYECT4

```text
controller_code = P4
purpose_code    = P4_EDUCATIONAL_RELATION
channel         = EMAIL
```

This purpose is intended for PROYECT4 information about educational resources, activities, initiatives and projects within the scope presented to the subscriber.

### San Blas educational information

```text
controller_code = SAN_BLAS
purpose_code    = SAN_BLAS_EDUCATIONAL_INFO
channel         = EMAIL
```

This covers the clearly described educational scope: materials/resources, educational visits and educational activities related to Reserva Ambiental San Blas.

### San Blas general updates

```text
controller_code = SAN_BLAS
purpose_code    = SAN_BLAS_GENERAL_UPDATES
channel         = EMAIL
```

This covers separately described general updates about the Reserve. It is not automatically granted by accepting educational information.

The v0.1 code `SAN_BLAS_EDUCATIONAL_VISITS` is deprecated and maps to `SAN_BLAS_EDUCATIONAL_INFO` before production data exists.

Before production use, `SAN_BLAS` must resolve to the exact legal entity that will act as controller/recipient for subsequent communication.

## Phone call -> email confirmation

A school, AMPA or other organisation may provide an email address during a telephone call and request that a confirmation message be sent to it.

P4CRM records the call as an interaction and creates a `CONSENT_REQUESTS` row plus one `CONSENT_REQUEST_SCOPES` row for every offered purpose.

```text
PHONE_CALL
    |
    v
CONSENT_REQUEST status=CREATED/SENT
    |
    v
confirmation email with one-time token
    |
    v
explicit web action from the supplied email address
    |
    v
CONSENT status=GRANTED + append-only CONSENT_EVENT
```

The call/request is not itself a `GRANTED` email consent in this workflow.

See [Email confirmation after a phone call](email-confirmation-flow.md).

## Confirmation-request security

The raw confirmation token is never persisted. Only its cryptographic digest is stored.

A request must be:

- scoped to a known contact point and target controller;
- tied to the exact text/privacy versions displayed;
- time-limited;
- single-use;
- confirmed only for purposes originally offered by the request.

If the recipient does nothing, no consent is granted.

## Evidence and history

`CONSENTS` represents current state. `CONSENT_EVENTS` is the append-only history used to reconstruct grants, withdrawals and other state changes.

For an email-confirmed grant, preserve at least:

- `contact_point_id`;
- controller;
- purpose;
- channel;
- grant timestamp;
- `request_id`;
- collection/confirmation source;
- form identifier;
- consent-text version;
- privacy-notice version;
- evidence reference when available.

The request itself also preserves its creation/sent/expiry/confirmation timestamps and its originating phone interaction when applicable.

## Transfer to San Blas

A completed transfer follows this chain:

```text
CONTACT_POINT
     |
     v
CONSENT for a SAN_BLAS purpose = GRANTED
     |
     v
DATA_TRANSFER: P4 -> SAN_BLAS
     |
     v
San Blas receives only the authorised data required for that purpose
```

Every completed `DATA_TRANSFERS` row contains the `consent_id` that authorised that purpose.

Accepting `SAN_BLAS_EDUCATIONAL_INFO` does not automatically authorise `SAN_BLAS_GENERAL_UPDATES`, and vice versa.

## Withdrawal and suppression

Withdrawal is scoped. For example:

```text
P4_EDUCATIONAL_RELATION     = GRANTED
SAN_BLAS_EDUCATIONAL_INFO   = GRANTED
SAN_BLAS_GENERAL_UPDATES    = REVOKED
```

A withdrawal or objection creates an append-only event and maintains the appropriate suppression state so that a later source import cannot silently reactivate the contact.

## Send-time rule

Campaign tooling evaluates eligibility at send time, not only when an audience is first created.

Conceptually:

```text
eligible =
  contact point is active
  AND the campaign's required permission/legal basis is valid
  AND no matching suppression exists
  AND campaign purpose matches the permission scope
```

The exact legal basis and operational rule for each campaign remains deployment-specific and must not be inferred solely from the presence of a contact record.
