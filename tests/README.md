# Tests

P4CRM tests will protect the data contract and privacy-critical workflow rules.

Initial test targets:

- required identifiers and foreign-key references;
- controlled enum values;
- duplicate contact-point detection;
- consent scope compatibility;
- suppression precedence;
- prevention of San Blas transfer without the required authorisation;
- audience exclusion when a matching suppression exists;
- import provenance requirements.

No production contact data should be used as test fixtures. Use synthetic examples only.
