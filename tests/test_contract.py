import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_contract.py"

spec = importlib.util.spec_from_file_location("validate_contract", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class ContractTests(unittest.TestCase):
    def test_repository_contract_is_valid(self):
        self.assertEqual([], validator.validate())

    def test_required_tables_are_declared(self):
        schema = validator.load_json(validator.SCHEMA_PATH)
        self.assertTrue(validator.REQUIRED_TABLES.issubset(schema["tables"]))

    def test_consent_scope_is_explicit(self):
        schema = validator.load_json(validator.SCHEMA_PATH)
        self.assertEqual(validator.REQUIRED_CONSENT_SCOPE, set(schema["consent_scope"]))

    def test_confirmation_request_does_not_replace_consent(self):
        schema = validator.load_json(validator.SCHEMA_PATH)
        self.assertIn("CONSENT_REQUESTS", schema["tables"])
        self.assertIn("CONSENT_REQUEST_SCOPES", schema["tables"])
        self.assertIn("CONSENT_EVENTS", schema["tables"])

    def test_partner_purposes_are_granular(self):
        schema = validator.load_json(validator.SCHEMA_PATH)
        purposes = set(schema["initial_purposes"])
        self.assertIn("PARTNER_EDUCATIONAL_INFO", purposes)
        self.assertIn("PARTNER_GENERAL_UPDATES", purposes)

    def test_partner_transfer_is_traceable_to_consent(self):
        schema = validator.load_json(validator.SCHEMA_PATH)
        fields = set(schema["tables"]["DATA_TRANSFERS"])
        self.assertIn("consent_id", fields)
        self.assertIn("to_controller_code", fields)
        self.assertIn("purpose_code", fields)


if __name__ == "__main__":
    unittest.main()
