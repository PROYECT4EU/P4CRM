"""Email confirmation helpers for consent requests.

The module is intentionally storage- and mail-provider-agnostic. A caller persists
records in P4CRM and sends the returned raw token only in the requested
confirmation email. The raw token must never be persisted or logged.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets
from typing import Iterable
from uuid import uuid4


DEFAULT_TTL_HOURS = 72


@dataclass(frozen=True)
class ConfirmationBundle:
    """Records to persist plus the one-time secret to deliver by email."""

    request: dict
    scopes: list[dict]
    token: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def token_digest(token: str) -> str:
    """Return the SHA-256 digest stored by P4CRM instead of the raw token."""

    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def token_matches(token: str, expected_digest: str) -> bool:
    """Constant-time comparison of a presented token with the stored digest."""

    return hmac.compare_digest(token_digest(token), expected_digest)


def create_confirmation_request(
    *,
    contact_point_id: str,
    organisation_id: str,
    destination: str,
    target_controller_code: str,
    purpose_codes: Iterable[str],
    sender_controller_code: str = "P4",
    origin_interaction_id: str | None = None,
    form_id: str,
    text_version: str,
    privacy_version: str,
    ttl_hours: int = DEFAULT_TTL_HOURS,
    now: datetime | None = None,
) -> ConfirmationBundle:
    """Create a pending email-confirmation request.

    This function does not grant consent. It creates a request whose offered
    scopes remain PENDING until an explicit confirmation action is completed.
    """

    if ttl_hours <= 0:
        raise ValueError("ttl_hours must be positive")

    purposes = list(dict.fromkeys(purpose_codes))
    if not purposes:
        raise ValueError("at least one purpose_code is required")

    created_at = now or utc_now()
    request_id = f"crq_{uuid4().hex}"
    token = secrets.token_urlsafe(32)

    request = {
        "request_id": request_id,
        "contact_point_id": contact_point_id,
        "organisation_id": organisation_id,
        "origin_interaction_id": origin_interaction_id or "",
        "sender_controller_code": sender_controller_code,
        "target_controller_code": target_controller_code,
        "channel": "EMAIL",
        "destination": destination,
        "status": "CREATED",
        "token_hash": token_digest(token),
        "created_at": iso(created_at),
        "sent_at": "",
        "expires_at": iso(created_at + timedelta(hours=ttl_hours)),
        "confirmed_at": "",
        "cancelled_at": "",
        "form_id": form_id,
        "text_version": text_version,
        "privacy_version": privacy_version,
        "evidence_ref": "",
        "notes": "",
    }

    scopes = [
        {
            "request_scope_id": f"crs_{uuid4().hex}",
            "request_id": request_id,
            "purpose_code": purpose,
            "decision": "PENDING",
            "decided_at": "",
            "consent_id": "",
            "notes": "",
        }
        for purpose in purposes
    ]

    return ConfirmationBundle(request=request, scopes=scopes, token=token)


def request_is_confirmable(request: dict, *, now: datetime | None = None) -> bool:
    """Return True only when a sent request is unused and not expired."""

    if request.get("status") not in {"CREATED", "SENT"}:
        return False

    expires_at = request.get("expires_at")
    if not expires_at:
        return False

    expires = datetime.fromisoformat(str(expires_at).replace("Z", "+00:00"))
    current = now or utc_now()
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    return current.astimezone(timezone.utc) < expires.astimezone(timezone.utc)


def mark_sent(request: dict, *, now: datetime | None = None) -> dict:
    """Return a copy of a request marked as sent."""

    if request.get("status") != "CREATED":
        raise ValueError("only CREATED requests can be marked SENT")
    updated = dict(request)
    updated["status"] = "SENT"
    updated["sent_at"] = iso(now or utc_now())
    return updated


def confirm_request(
    *,
    request: dict,
    scopes: Iterable[dict],
    presented_token: str,
    granted_purpose_codes: Iterable[str],
    now: datetime | None = None,
) -> tuple[dict, list[dict], list[dict], list[dict]]:
    """Confirm selected scopes and produce consent state + append-only events.

    Returns ``(updated_request, updated_scopes, consents, consent_events)``.
    Unselected offered scopes become NOT_GRANTED; they do not silently become
    consent. The caller should persist all returned records atomically.
    """

    current = now or utc_now()
    if not request_is_confirmable(request, now=current):
        raise ValueError("request is not confirmable")
    if not token_matches(presented_token, request.get("token_hash", "")):
        raise ValueError("invalid confirmation token")

    offered = {scope["purpose_code"]: dict(scope) for scope in scopes}
    granted = set(granted_purpose_codes)
    unknown = granted - set(offered)
    if unknown:
        raise ValueError(f"purpose not offered by request: {sorted(unknown)}")

    decided_at = iso(current)
    updated_scopes: list[dict] = []
    consents: list[dict] = []
    events: list[dict] = []

    for purpose, scope in offered.items():
        if scope.get("decision") != "PENDING":
            raise ValueError("request scope has already been decided")

        scope["decided_at"] = decided_at
        if purpose not in granted:
            scope["decision"] = "NOT_GRANTED"
            updated_scopes.append(scope)
            continue

        consent_id = f"con_{uuid4().hex}"
        scope["decision"] = "GRANTED"
        scope["consent_id"] = consent_id
        updated_scopes.append(scope)

        consent = {
            "consent_id": consent_id,
            "contact_point_id": request["contact_point_id"],
            "controller_code": request["target_controller_code"],
            "purpose_code": purpose,
            "channel": "EMAIL",
            "status": "GRANTED",
            "granted_at": decided_at,
            "revoked_at": "",
            "source_type": "EMAIL_CONFIRMATION",
            "form_id": request["form_id"],
            "text_version": request["text_version"],
            "privacy_version": request["privacy_version"],
            "evidence_ref": request.get("evidence_ref", ""),
            "notes": "",
        }
        consents.append(consent)

        events.append(
            {
                "consent_event_id": f"cev_{uuid4().hex}",
                "consent_id": consent_id,
                "contact_point_id": request["contact_point_id"],
                "controller_code": request["target_controller_code"],
                "purpose_code": purpose,
                "channel": "EMAIL",
                "event_type": "GRANTED",
                "occurred_at": decided_at,
                "source_type": "EMAIL_CONFIRMATION",
                "request_id": request["request_id"],
                "text_version": request["text_version"],
                "privacy_version": request["privacy_version"],
                "evidence_ref": request.get("evidence_ref", ""),
                "notes": "",
            }
        )

    updated_request = dict(request)
    updated_request["status"] = "CONFIRMED"
    updated_request["confirmed_at"] = decided_at

    return updated_request, updated_scopes, consents, events
