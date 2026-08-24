import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from p4crm.confirmation import (  # noqa: E402
    confirm_request,
    create_confirmation_request,
    mark_sent,
    request_is_confirmable,
    token_matches,
)


class ConfirmationTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 8, 24, 21, 45, tzinfo=timezone.utc)
        self.bundle = create_confirmation_request(
            contact_point_id="cp_test",
            organisation_id="org_test",
            destination="school@example.org",
            target_controller_code="PARTNER",
            purpose_codes=["PARTNER_EDUCATIONAL_INFO", "PARTNER_GENERAL_UPDATES"],
            origin_interaction_id="int_phone_1",
            form_id="PARTNER_CONFIRM_V1",
            text_version="PARTNER_CONFIRM_TEXT_V1",
            privacy_version="PRIVACY_V1",
            now=self.now,
        )

    def test_raw_token_is_not_persisted(self):
        self.assertNotEqual(self.bundle.token, self.bundle.request["token_hash"])
        self.assertTrue(token_matches(self.bundle.token, self.bundle.request["token_hash"]))
        self.assertNotIn(self.bundle.token, self.bundle.request.values())

    def test_request_starts_without_granted_scope(self):
        self.assertEqual("CREATED", self.bundle.request["status"])
        self.assertTrue(all(scope["decision"] == "PENDING" for scope in self.bundle.scopes))

    def test_selected_scope_only_becomes_consent(self):
        sent = mark_sent(self.bundle.request, now=self.now + timedelta(minutes=1))
        confirmed, scopes, consents, events = confirm_request(
            request=sent,
            scopes=self.bundle.scopes,
            presented_token=self.bundle.token,
            granted_purpose_codes=["PARTNER_EDUCATIONAL_INFO"],
            now=self.now + timedelta(minutes=2),
        )

        self.assertEqual("CONFIRMED", confirmed["status"])
        decisions = {scope["purpose_code"]: scope["decision"] for scope in scopes}
        self.assertEqual("GRANTED", decisions["PARTNER_EDUCATIONAL_INFO"])
        self.assertEqual("NOT_GRANTED", decisions["PARTNER_GENERAL_UPDATES"])
        self.assertEqual(1, len(consents))
        self.assertEqual("PARTNER_EDUCATIONAL_INFO", consents[0]["purpose_code"])
        self.assertEqual("EMAIL_CONFIRMATION", consents[0]["source_type"])
        self.assertEqual(1, len(events))
        self.assertEqual(sent["request_id"], events[0]["request_id"])

    def test_invalid_token_is_rejected(self):
        sent = mark_sent(self.bundle.request, now=self.now)
        with self.assertRaises(ValueError):
            confirm_request(
                request=sent,
                scopes=self.bundle.scopes,
                presented_token="wrong-token",
                granted_purpose_codes=["PARTNER_EDUCATIONAL_INFO"],
                now=self.now + timedelta(minutes=1),
            )

    def test_expired_request_is_not_confirmable(self):
        future = self.now + timedelta(hours=73)
        self.assertFalse(request_is_confirmable(self.bundle.request, now=future))

    def test_unknown_scope_is_rejected(self):
        sent = mark_sent(self.bundle.request, now=self.now)
        with self.assertRaises(ValueError):
            confirm_request(
                request=sent,
                scopes=self.bundle.scopes,
                presented_token=self.bundle.token,
                granted_purpose_codes=["NOT_OFFERED"],
                now=self.now + timedelta(minutes=1),
            )


if __name__ == "__main__":
    unittest.main()
