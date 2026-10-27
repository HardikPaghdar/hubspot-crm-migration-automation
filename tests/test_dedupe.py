from hubspot_migration.dedupe import find_duplicate_emails
from hubspot_migration.migration import prepare_contacts


def test_duplicate_detection_is_case_insensitive_and_keeps_first():
    rows = [{"email": "A@example.com"}, {"email": "a@EXAMPLE.com"}, {"email": "b@example.com"}]
    assert find_duplicate_emails(rows) == {1}


def test_prepare_contacts_separates_ready_duplicate_and_invalid_rows():
    rows = [
        {"Email Address": "one@example.com", "First Name": "One"},
        {"Email Address": "ONE@example.com", "First Name": "Duplicate"},
        {"Email Address": "invalid", "First Name": "Bad"},
    ]
    result = prepare_contacts(rows)
    assert len(result["ready"]) == 1
    assert len(result["duplicates"]) == 1
    assert len(result["rejected"]) == 1
