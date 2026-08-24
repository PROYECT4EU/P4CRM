# Email confirmation after a phone call — v0.2

This document defines the P4CRM flow for a school, AMPA or other organisation that provides an email address during a telephone conversation and asks to receive a confirmation message before any recurring email information is enabled.

The telephone conversation can initiate the request, but recurring email permission is only activated after an affirmative action performed through the confirmation flow sent to the supplied email address.

## 1. Phone interaction

The call is stored as an `INTERACTIONS` record:

```text
interaction_type = PHONE_CALL
direction        = OUTBOUND or INBOUND
outcome          = CONFIRMATION_EMAIL_REQUESTED
```

The operator records the address supplied by the organisation and confirms verbally that a short confirmation email will be sent to it.

The call itself must not silently create a `GRANTED` email consent when this confirmation workflow is used.

## 2. Create the confirmation request

P4CRM creates:

```text
CONSENT_REQUESTS
CONSENT_REQUEST_SCOPES
```

The request contains the email contact point, organisation, originating interaction, sender, target controller, exact form/text/privacy versions and an expiry time.

A request may offer one or more independent scopes. Generic partner scopes are:

### `PARTNER_EDUCATIONAL_INFO`

Information about clearly described educational materials/resources, educational visits and educational activities offered by the configured partner.

### `PARTNER_GENERAL_UPDATES`

General updates from that partner, such as news, projects, activities and other clearly described information.

These scopes are separated because educational information and broader general updates do not need to be accepted together.

If PROYECT4 also seeks permission for its own educational relationship, `P4_EDUCATIONAL_RELATION` is presented as a separate scope and is not silently bundled into partner permission.

## 3. One-time token

The confirmation service generates a cryptographically random opaque token.

Rules:

- the raw token is sent only in the confirmation link;
- the raw token is never stored in P4CRM and must not be logged;
- P4CRM stores only a SHA-256 digest in `CONSENT_REQUESTS.token_hash`;
- the token expires (default implementation: 72 hours);
- the request is single-use;
- a confirmed, cancelled or expired request cannot be reused.

Example URL shape:

```text
https://<confirmation-host>/consent/confirm?t=<opaque-token>
```

The email address itself must not be included in the URL or in UTM parameters.

## 4. Confirmation email

The message is a confirmation requested during the telephone conversation and should be narrowly limited to that purpose.

Recommended characteristics:

- identify PROYECT4 as the sender/manager of the confirmation process;
- explain that the message is being sent because the address was provided/requested during the prior interaction;
- identify the exact configured legal entity that will be the partner controller/recipient before production launch;
- summarise the scopes that can be selected;
- provide one confirmation/preferences link;
- avoid unrelated promotional content;
- provide a way to ignore/cancel the request and a privacy-information link.

If the recipient does nothing, no recurring-email consent is granted.

## 5. Confirmation page

The page validates the token and displays the address being confirmed without placing it in the public URL.

It must show the configured controller identity and relevant information notice before the affirmative action.

Conceptual form:

```text
Email to confirm: school@example.org

[ ] I want to receive educational materials, resources, visits and
    educational activities from the partner organisation.

[ ] I want to receive general updates, projects and activities from
    the partner organisation.

[Confirm preferences]
```

The boxes are not preselected.

The exact production wording must use the verified legal identity configured for `PARTNER`.

## 6. Atomic confirmation

When the user submits the form:

1. validate that the request exists;
2. compare the presented token against the stored digest using a constant-time comparison;
3. verify that the request is unused and not expired;
4. verify that every submitted purpose was offered by the request;
5. mark selected scopes `GRANTED`;
6. leave unselected scopes `NOT_GRANTED`;
7. create/update the corresponding `CONSENTS` current-state record;
8. append a `CONSENT_EVENTS` record for every grant;
9. mark the request `CONFIRMED` and set `confirmed_at`;
10. persist the changes atomically.

`src/p4crm/confirmation.py` implements the storage-agnostic domain portion of this workflow.

## 7. Transfer to a partner

If PROYECT4 collected the confirmation for a different configured controller, an authorised transfer can only be created for scopes actually granted.

```text
PHONE_CALL
    |
    v
CONSENT_REQUEST
    |
    v
CONFIRMATION EMAIL
    |
    v
AFFIRMATIVE WEB ACTION
    |
    v
CONSENT + CONSENT_EVENT
    |
    v
DATA_TRANSFER: P4 -> PARTNER
```

A transfer row references the `consent_id` that authorises the relevant purpose.

## 8. Withdrawal

Every later recurring email must be evaluated against current consent and suppression state at send time.

Withdrawal creates a `REVOKED` consent event and the corresponding suppression so that later imports do not silently reactivate the address.

## 9. Deployment note

`PARTNER` is deliberately generic in the public repository. Each deployment must configure the exact partner legal entity, privacy information, purposes and wording before production use.

The implementation supports demonstrability and granular consent; it is not itself a legal determination for every deployment or campaign.
