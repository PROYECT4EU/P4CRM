#!/usr/bin/env python3
"""Prepare an institutional CSV import for P4CRM v0.2.

This script performs local/staging normalisation only. It does not send email,
grant consent or write directly to the production CRM.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from p4crm.importer import build_import_row  # noqa: E402


REQUIRED_COLUMNS = {"organisation_name", "email"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--source-name", required=True)
    parser.add_argument("--source-type", default="PUBLIC_DIRECTORY")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--publisher", default="")
    parser.add_argument("--retrieved-at", required=True)
    parser.add_argument("--identifier-scheme", default="")
    parser.add_argument("--default-organisation-type", default="SCHOOL")
    parser.add_argument("--default-country", default="ES")
    parser.add_argument("--default-region", default="Canarias")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    accepted_path = args.output_dir / "accepted.jsonl"
    rejected_path = args.output_dir / "rejected.jsonl"

    accepted = 0
    rejected = 0

    with args.input_csv.open("r", encoding="utf-8-sig", newline="") as source_handle:
        reader = csv.DictReader(source_handle)
        fieldnames = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - fieldnames
        if missing:
            raise SystemExit(f"missing required CSV columns: {sorted(missing)}")

        with accepted_path.open("w", encoding="utf-8") as accepted_handle, rejected_path.open(
            "w", encoding="utf-8"
        ) as rejected_handle:
            for row_number, row in enumerate(reader, start=2):
                try:
                    bundle = build_import_row(
                        source_name=args.source_name,
                        source_type=args.source_type,
                        source_url=args.source_url,
                        publisher=args.publisher,
                        retrieved_at=args.retrieved_at,
                        organisation_name=row.get("organisation_name", ""),
                        organisation_type=row.get("organisation_type") or args.default_organisation_type,
                        email=row.get("email", ""),
                        country=row.get("country") or args.default_country,
                        region=row.get("region") or args.default_region,
                        island=row.get("island", ""),
                        municipality=row.get("municipality", ""),
                        postal_code=row.get("postal_code", ""),
                        address=row.get("address", ""),
                        website=row.get("website", ""),
                        external_id=row.get("external_id", ""),
                        identifier_scheme=row.get("identifier_scheme") or args.identifier_scheme,
                        is_generic=(row.get("is_generic", "true").strip().lower() not in {"0", "false", "no"}),
                    )
                    payload = {
                        "source": bundle.source,
                        "organisation": bundle.organisation,
                        "identifier": bundle.identifier,
                        "contact_point": bundle.contact_point,
                        "contact_point_source": bundle.contact_point_source,
                        "prospect": bundle.prospect,
                    }
                    accepted_handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
                    accepted += 1
                except Exception as exc:  # row-level quarantine; preserve source line locally
                    rejected_handle.write(
                        json.dumps(
                            {"row_number": row_number, "error": str(exc), "row": row},
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
                    rejected += 1

    print(f"accepted={accepted} rejected={rejected}")
    print(f"accepted_output={accepted_path}")
    print(f"rejected_output={rejected_path}")
    return 0 if accepted else 2


if __name__ == "__main__":
    raise SystemExit(main())
