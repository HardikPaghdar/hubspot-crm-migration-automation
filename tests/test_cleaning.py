from hubspot_migration.cleaning import normalize_contact, normalize_phone, validate_contact


def test_normalize_contact_maps_common_headers():
    row = normalize_contact({"First Name": " Ava ", "Email Address": " AVA@EXAMPLE.COM ", "Phone Number": "+1 (415) 555-0134"})
    assert row["firstname"] == "Ava"
    assert row["email"] == "ava@example.com"
    assert row["phone"] == "+14155550134"


def test_validate_contact_flags_invalid_email():
    assert validate_contact({"email": "nope"}) == ["invalid_email"]


def test_validate_contact_flags_missing_email():
    assert validate_contact({}) == ["missing_email"]


def test_normalize_phone_handles_blank_and_plain_digits():
    assert normalize_phone("") == ""
    assert normalize_phone("415.555.0100") == "4155550100"
