#!/usr/bin/env python3
"""Validate the repository-level P4CRM v0.2 data contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "p4crm-v0.2.json"
ENUMS_PATH = ROOT / "config" / "enums.json"

REQUIRED_TABLES = {
    "ORGANISATIONS", "ORGANISATION_IDENTIFIERS", "CONTACT_POINTS",
    "CONTACT_POINT_SOURCES", "PEOPLE", "SOURCES", "IMPORT_BATCHES",
    "PROSPECTS", "CONSENTS", "CONSENT_EVENTS", "CONSENT_REQUESTS",
    "CONSENT_REQUEST_SCOPES", "SUPPRESSIONS", "INTERACTIONS",
    "CAMPAIGNS", "DATA_TRANSFERS", "PROJECTS", "OPPORTUNITIES",
}

REQUIRED_CONSENT_SCOPE = {
    "contact_point_id", "controller_code", "purpose_code", "channel",
}

REQUIRED_PURPOSES = {
    "P4_EDUCATIONAL_RELATION",
    "PARTNER_EDUCATIONAL_INFO",
    "PARTNER_GENERAL_UPDATES",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate() -> list[str]:
    errors: list[str] = []
    schema = load_json(SCHEMA_PATH)
    enums = load_json(ENUMS_PATH)

    if schema.get("schema_version") != "0.2":
        errors.append("schema_version must be 0.2")

    tables = schema.get("tables", {})
    missing_tables = REQUIRED_TABLES - set(tables)
    if missing_tables:
        errors.append(f"missing tables: {sorted(missing_tables)}")

    for table_name, fields in tables.items():
        if not isinstance(fields, list) or not fields:
            errors.append(f"{table_name}: fields must be a non-empty list")
            continue
        if len(fields) != len(set(fields)):
            errors.append(f"{table_name}: duplicate field names")
        if not fields[0].endswith("_id") and table_name != "PROJECTS":
            errors.append(f"{table_name}: first field should be the stable identifier")

    if set(schema.get("consent_scope", [])) != REQUIRED_CONSENT_SCOPE:
        errors.append("consent_scope does not match the v0.2 scoped-consent contract")

    consent_fields = set(tables.get("CONSENTS", []))
    if not REQUIRED_CONSENT_SCOPE.issubset(consent_fields):
        errors.append("CONSENTS is missing one or more consent-scope fields")

    event_fields = set(tables.get("CONSENT_EVENTS", []))
    for required in REQUIRED_CONSENT_SCOPE | {"consent_id", "event_type", "occurred_at", "request_id"}:
        if required not in event_fields:
            errors.append(f"CONSENT_EVENTS is missing {required}")

    request_fields = set(tables.get("CONSENT_REQUESTS", []))
    for required in {
        "contact_point_id", "origin_interaction_id", "sender_controller_code",
        "target_controller_code", "destination", "status", "token_hash",
        "expires_at", "text_version", "privacy_version"
    }:
        if required not in request_fields:
            errors.append(f"CONSENT_REQUESTS is missing {required}")

    request_scope_fields = set(tables.get("CONSENT_REQUEST_SCOPES", []))
    for required in {"request_id", "purpose_code", "decision", "consent_id"}:
        if required not in request_scope_fields:
            errors.append(f"CONSENT_REQUEST_SCOPES is missing {required}")

    import_fields = set(tables.get("IMPORT_BATCHES", []))
    for required in {"source_id", "imported_at", "importer_version", "accepted_count", "rejected_count", "status"}:
        if required not in import_fields:
            errors.append(f"IMPORT_BATCHES is missing {required}")

    contact_source_fields = set(tables.get("CONTACT_POINT_SOURCES", []))
    for required in {"contact_point_id", "source_id", "first_seen_at", "last_seen_at"}:
        if required not in contact_source_fields:
            errors.append(f"CONTACT_POINT_SOURCES is missing {required}")

    transfer_fields = set(tables.get("DATA_TRANSFERS", []))
    for required in {"consent_id", "from_controller_code", "to_controller_code", "purpose_code"}:
        if required not in transfer_fields:
            errors.append(f"DATA_TRANSFERS is missing {required}")

    purposes = set(schema.get("initial_purposes", []))
    if not REQUIRED_PURPOSES.issubset(purposes):
        errors.append("initial_purposes is missing a required v0.2 purpose")
    if purposes != set(enums.get("initial_purposes", [])):
        errors.append("schema and enum initial_purposes do not match")

    aliases = schema.get("deprecated_purpose_aliases", {})
    if aliases.get("PARTNER_EDUCATIONAL_VISITS") != "PARTNER_EDUCATIONAL_INFO":
        errors.append("v0.1 partner-purpose migration alias is missing")

    if "EMAIL_CONFIRMATION" not in enums.get("consent_source_types", []):
        errors.append("consent_source_types must include EMAIL_CONFIRMATION")
    if "CONFIRMED" not in enums.get("consent_request_status", []):
        errors.append("consent_request_status must include CONFIRMED")
    if "PENDING" not in enums.get("consent_request_scope_decision", []):
        errors.append("consent_request_scope_decision must include PENDING")
    if "UNSUBSCRIBED" not in enums.get("suppression_reasons", []):
        errors.append("suppression_reasons must include UNSUBSCRIBED")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("P4CRM contract validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("P4CRM contract validation OK (schema v0.2)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
