import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from p4crm.importer import build_import_row, normalise_email  # noqa: E402


class ImporterTests(unittest.TestCase):
    def test_email_is_canonicalised(self):
        self.assertEqual("centro@example.org", normalise_email("  Centro@Example.ORG "))

    def test_invalid_email_is_rejected(self):
        with self.assertRaises(ValueError):
            normalise_email("not-an-email")

    def test_same_official_centre_reuses_stable_ids(self):
        kwargs = dict(
            source_name="Directorio oficial de centros",
            source_type="PUBLIC_DIRECTORY",
            source_url="https://example.org/centros",
            publisher="Administración educativa",
            retrieved_at="2026-08-24T20:00:00Z",
            organisation_name="CEIP Ejemplo",
            organisation_type="SCHOOL",
            email="38000000@example.org",
            island="Tenerife",
            municipality="Ejemplo",
            external_id="38000000",
            identifier_scheme="CANARY_EDU_CENTRE_CODE",
            now="2026-08-24T20:00:00Z",
        )
        first = build_import_row(**kwargs)
        second = build_import_row(**{**kwargs, "retrieved_at": "2026-09-01T20:00:00Z"})
        self.assertEqual(first.organisation["organisation_id"], second.organisation["organisation_id"])
        self.assertEqual(first.contact_point["contact_point_id"], second.contact_point["contact_point_id"])
        self.assertEqual(first.prospect["prospect_id"], second.prospect["prospect_id"])

    def test_import_never_creates_consent(self):
        row = build_import_row(
            source_name="Directory",
            source_type="PUBLIC_DIRECTORY",
            source_url="https://example.org/directory",
            publisher="Publisher",
            retrieved_at="2026-08-24T20:00:00Z",
            organisation_name="AMPA Example",
            organisation_type="AMPA",
            email="ampa@example.org",
            now="2026-08-24T20:00:00Z",
        )
        self.assertFalse(hasattr(row, "consent"))
        self.assertEqual("NEW", row.prospect["relationship_status"])

    def test_contact_point_source_preserves_provenance(self):
        row = build_import_row(
            source_name="Directory",
            source_type="PUBLIC_DIRECTORY",
            source_url="https://example.org/directory",
            publisher="Publisher",
            retrieved_at="2026-08-24T20:00:00Z",
            organisation_name="IES Example",
            organisation_type="SCHOOL",
            email="ies@example.org",
            now="2026-08-24T20:00:00Z",
        )
        self.assertEqual(row.contact_point["contact_point_id"], row.contact_point_source["contact_point_id"])
        self.assertEqual(row.source["source_id"], row.contact_point_source["source_id"])


if __name__ == "__main__":
    unittest.main()
