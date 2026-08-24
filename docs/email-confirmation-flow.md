# Email confirmation after a phone call — v0.2

This document defines the P4CRM flow for a school, AMPA or other organisation that provides an email address during a telephone conversation and asks to receive a confirmation message before any recurring email information is enabled.

The goal is both operational and evidential: **the telephone conversation can initiate the request, but recurring email permission is only activated after an affirmative action performed from the supplied email address**.

## 1. Phone interaction

The call is stored as an `INTERACTIONS` record:

```text
interaction_type = PHONE_CALL
direction        = OUTBOUND or INBOUND
outcome          = CONFIRMATION_EMAIL_REQUESTED
```

The operator records the email address supplied by the organisation and confirms verbally that a short confirmation email will be sent to that address.

The call itself must not silently create a `GRANTED` email consent when this confirmation workflow is being used.

## 2. Create the confirmation request

P4CRM creates:

```text
CONSENT_REQUESTS
CONSENT_REQUEST_SCOPES
```

The request contains the email contact point, the organisation, the originating phone interaction, the sender, the target controller, the exact form/text/privacy versions and an expiry time.

The request may offer one or more independent scopes.

For the initial San Blas case the recommended scopes are:

### `SAN_BLAS_EDUCATIONAL_INFO`

Information about educational materials and resources, educational visits and educational activities related to Reserva Ambiental San Blas.

### `SAN_BLAS_GENERAL_UPDATES`

General updates about Reserva Ambiental San Blas, such as news, projects, activities and other clearly described information related to the Reserve.

These scopes are separated because educational information and broader general updates do not need to be accepted together.

If PROYECT4 also wants permission for its own educational relationship, that must be presented as a separate `P4_EDUCATIONAL_RELATION` scope and must not be silently bundled into the San Blas confirmation.

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

The email address itself must **not** be included in the URL or in UTM parameters.

## 4. Confirmation email

The message is a confirmation requested during the telephone conversation. It should be narrowly limited to that purpose.

Recommended characteristics:

- identify PROYECT4 as the sender/manager of the confirmation process;
- explain that the message is being sent because the address was provided during the call;
- identify the exact legal entity that will be the controller/recipient for San Blas communications before production launch;
- summarise the scopes that can be selected;
- provide one confirmation/preferences link;
- avoid prices, discounts, booking offers or unrelated promotional content;
- provide a way to ignore/cancel the request and a privacy-information link.

If the person does nothing, no recurring-email consent is granted.

## 5. Confirmation page

The confirmation page validates the token and displays the address being confirmed without placing it in the public URL.

It must show the controller identity and the relevant information notice before the affirmative action.

Conceptual form:

```text
Correo a confirmar: colegio@example.org

[ ] Quiero recibir información sobre materiales, recursos, visitas y
    actividades educativas de Reserva Ambiental San Blas.

[ ] Quiero recibir novedades, proyectos, actividades y otra información
    general de interés sobre Reserva Ambiental San Blas.

[Confirmar preferencias]
```

The boxes are not preselected.

The exact production wording must use the verified legal identity behind the `SAN_BLAS` controller code.

## 6. Atomic confirmation

When the user submits the form:

1. validate that the request exists;
2. compare the presented token against the stored digest using a constant-time comparison;
3. verify that the request is unused and not expired;
4. verify that every submitted purpose was actually offered by the request;
5. mark selected scopes `GRANTED`;
6. leave unselected scopes `NOT_GRANTED`;
7. create/update the corresponding `CONSENTS` current-state record;
8. append a `CONSENT_EVENTS` record for every grant;
9. mark the request `CONFIRMED` and set `confirmed_at`;
10. persist the changes atomically.

`src/p4crm/confirmation.py` implements the storage-agnostic domain portion of this workflow.

## 7. Transfer to San Blas

If PROYECT4 is the system that collected the confirmation for a different controller, an authorised transfer can only be created for scopes actually granted.

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
DATA_TRANSFER: P4 -> SAN_BLAS
```

A transfer row references the `consent_id` that authorises the relevant purpose.

## 8. Withdrawal

Every later recurring email must be evaluated against the current consent and suppression state at send time.

Withdrawal must be straightforward. A withdrawal creates a `REVOKED` consent event and the corresponding suppression so that later imports do not silently reactivate the address.

## 9. Legal implementation notes

The implementation is designed to support demonstrability and granular consent; it is not itself a legal determination for every deployment.

Relevant primary/authority references include:

- GDPR Article 7: the controller must be able to demonstrate consent, requests must be clear, and withdrawal must be as easy as giving consent: https://eur-lex.europa.eu/eli/reg/2016/679/2016-05-04/eng
- AEPD consent FAQ: consent requires an affirmative action, must be informed and demonstrable, and purposes should be separated when appropriate: https://www.aepd.es/preguntas-frecuentes/2-tus-obligaciones-como-responsable-del-tratamiento/5-bases-legitimadoras-del-tratamiento/FAQ-0211-segun-el-rgpd-como-debe-solicitarse-el-consentimiento-de-los-interesados-para-tratar-sus-datos-personales
- LSSI Article 21: promotional email must have been previously requested or expressly authorised, subject to the statutory exceptions: https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758#a21

The production confirmation email should only be sent when the recipient has requested or authorised that confirmation step, for example during the documented telephone conversation.
