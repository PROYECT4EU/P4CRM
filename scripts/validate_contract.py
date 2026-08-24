#!/usr/bin/env python3
"""Validate the repository-level P4CRM v0.1 data contract.

This validator intentionally uses only the Python standard library so it can run
locally or in CI without installing dependencies.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "p4crm-v0.1.json"
ENUMS_PATH = ROOT / "config" / "enums.json"

REQUIRED_TABLES = {
    "ORGANISATIONS",
    "CONTACT_POINTS",
    "PEOPLE",
    "SOURCES",
    "PROSPECTS",
    "CONSENTS",
    "SUPPRESSIONS",
    "INTERACTIONS",
    "CAMPAIGNS",
    "DATA_TRANSFERS",
    "PROJECTS",
    "OPPORTUNITIES",
}

REQUIRED_CONSENT_SCOPE = {
    "contact_point_id",
    "controller_code",
    "purpose_code",
    "channel",
}

REQUIRED_PURPOSES = {
    "P4_EDUCATIONAL_RELATION",
    "SAN_BLAS_EDUCATIONAL_VISITS",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate() -> list[str]:
    errors: list[str] = []
    schema = load_json(SCHEMA_PATH)
    enums = load_json(ENUMS_PATH)

    if schema.get("schema_version") != "0.1":
        errors.append("schema_version must be 0.1")

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

    consent_scope = set(schema.get("consent_scope", []))
    if consent_scope != REQUIRED_CONSENT_SCOPE:
        errors.append("consent_scope does not match the v0.1 scoped-consent contract")

    consent_fields = set(tables.get("CONSENTS", []))
    if not REQUIRED_CONSENT_SCOPE.issubset(consent_fields):
        errors.append("CONSENTS is missing one or more consent-scope fields")

    transfer_fields = set(tables.get("DATA_TRANSFERS", []))
    for required in {"consent_id", "from_controller_code", "to_controller_code", "purpose_code"}:
        if required not in transfer_fields:
            errors.append(f"DATA_TRANSFERS is missing {required}")

    purposes = set(schema.get("initial_purposes", []))
    if not REQUIRED_PURPOSES.issubset(purposes):
        errors.append("initial_purposes is missing a required v0.1 purpose")

    enum_purposes = set(enums.get("initial_purposes", []))
    if purposes != enum_purposes:
        errors.append("schema and enum initial_purposes do not match")

    if "GRANTED" not in enums.get("consent_status", []):
        errors.append("consent_status must include GRANTED")
    if "REVOKED" not in enums.get("consent_status", []):
        errors.append("consent_status must include REVOKED")
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

    print("P4CRM contract validation OK (schema v0.1)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
