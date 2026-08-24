"""Normalisation helpers for institutional/professional source imports."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re
import unicodedata
from urllib.parse import urlsplit, urlunsplit
from uuid import NAMESPACE_URL, uuid5


EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@dataclass(frozen=True)
class NormalisedImportRow:
    source: dict
    organisation: dict
    identifier: dict | None
    contact_point: dict
    contact_point_source: dict
    prospect: dict


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalise_space(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value or "").strip().split())


def normalise_email(value: str) -> str:
    email = normalise_space(value).lower()
    if not EMAIL_RE.fullmatch(email):
        raise ValueError(f"invalid email: {value!r}")
    return email


def normalise_url(value: str) -> str:
    value = normalise_space(value)
    if not value:
        return ""
    parts = urlsplit(value if "://" in value else f"https://{value}")
    if not parts.hostname:
        raise ValueError(f"invalid URL: {value!r}")
    scheme = parts.scheme.lower() or "https"
    host = parts.hostname.lower()
    port = f":{parts.port}" if parts.port else ""
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((scheme, host + port, path, parts.query, ""))


def stable_id(prefix: str, *parts: str) -> str:
    key = "|".join(normalise_space(part).casefold() for part in parts)
    return f"{prefix}_{uuid5(NAMESPACE_URL, key).hex}"


def organisation_match_key(
    *,
    name: str,
    municipality: str = "",
    region: str = "",
    external_id: str = "",
    identifier_scheme: str = "",
) -> str:
    """Build the deterministic identity key used by the staging importer.

    A trusted external centre/organisation identifier wins over fuzzy name-based
    matching. Name-based identity is deliberately conservative and should be
    reviewed before merging ambiguous organisations.
    """

    if external_id:
        return "external:" + normalise_space(identifier_scheme or "SOURCE") + ":" + normalise_space(external_id)
    return "name:" + "|".join(
        [normalise_space(name).casefold(), normalise_space(municipality).casefold(), normalise_space(region).casefold()]
    )


def build_import_row(
    *,
    source_name: str,
    source_type: str,
    source_url: str,
    publisher: str,
    retrieved_at: str,
    organisation_name: str,
    organisation_type: str,
    email: str,
    country: str = "ES",
    region: str = "Canarias",
    island: str = "",
    municipality: str = "",
    postal_code: str = "",
    address: str = "",
    website: str = "",
    external_id: str = "",
    identifier_scheme: str = "",
    is_generic: bool = True,
    project_code: str = "P4",
    segment: str = "EDUCATION",
    now: str | None = None,
) -> NormalisedImportRow:
    """Convert one source row into deterministic P4CRM v0.2 records.

    The function never creates a GRANTED consent.
    """

    if not normalise_space(source_name):
        raise ValueError("source_name is required")
    if not normalise_space(organisation_name):
        raise ValueError("organisation_name is required")

    email_value = normalise_email(email)
    canonical_source_url = normalise_url(source_url) if source_url else ""
    canonical_website = normalise_url(website) if website else ""
    timestamp = now or utc_iso()

    source_key = canonical_source_url or f"{publisher}|{source_name}"
    source_id = stable_id("src", source_type, source_key)

    org_key = organisation_match_key(
        name=organisation_name,
        municipality=municipality,
        region=region,
        external_id=external_id,
        identifier_scheme=identifier_scheme,
    )
    organisation_id = stable_id("org", org_key)
    contact_point_id = stable_id("cp", organisation_id, "EMAIL", email_value)
    prospect_id = stable_id("pr", organisation_id, project_code)
    contact_point_source_id = stable_id("cps", contact_point_id, source_id)

    source = {
        "source_id": source_id,
        "source_type": source_type,
        "source_name": normalise_space(source_name),
        "source_url": canonical_source_url,
        "publisher": normalise_space(publisher),
        "retrieved_at": retrieved_at,
        "licence_or_terms": "",
        "notes": "",
    }

    organisation = {
        "organisation_id": organisation_id,
        "name": normalise_space(organisation_name),
        "legal_name": "",
        "organisation_type": organisation_type,
        "country": normalise_space(country),
        "region": normalise_space(region),
        "island": normalise_space(island),
        "municipality": normalise_space(municipality),
        "postal_code": normalise_space(postal_code),
        "address": normalise_space(address),
        "website": canonical_website,
        "status": "ACTIVE",
        "created_at": timestamp,
        "updated_at": timestamp,
        "notes": "",
    }

    identifier = None
    if external_id:
        scheme = normalise_space(identifier_scheme or "SOURCE")
        identifier = {
            "identifier_id": stable_id("oid", organisation_id, scheme, external_id),
            "organisation_id": organisation_id,
            "scheme": scheme,
            "value": normalise_space(external_id),
            "source_id": source_id,
            "is_primary": True,
            "created_at": timestamp,
            "notes": "",
        }

    contact_point = {
        "contact_point_id": contact_point_id,
        "organisation_id": organisation_id,
        "person_id": "",
        "contact_type": "EMAIL",
        "value": email_value,
        "label": "institutional" if is_generic else "professional",
        "is_generic": bool(is_generic),
        "source_id": source_id,
        "verified_at": retrieved_at,
        "status": "ACTIVE",
        "created_at": timestamp,
        "updated_at": timestamp,
    }

    contact_point_source = {
        "contact_point_source_id": contact_point_source_id,
        "contact_point_id": contact_point_id,
        "source_id": source_id,
        "first_seen_at": retrieved_at,
        "last_seen_at": retrieved_at,
        "source_reference": canonical_source_url,
        "notes": "",
    }

    prospect = {
        "prospect_id": prospect_id,
        "organisation_id": organisation_id,
        "project_code": project_code,
        "source_id": source_id,
        "segment": segment,
        "priority": "MEDIUM",
        "relationship_status": "NEW",
        "interests": "",
        "owner": "",
        "created_at": timestamp,
        "updated_at": timestamp,
        "notes": "",
    }

    return NormalisedImportRow(
        source=source,
        organisation=organisation,
        identifier=identifier,
        contact_point=contact_point,
        contact_point_source=contact_point_source,
        prospect=prospect,
    )
