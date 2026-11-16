"""Validate Login service input (Robert)."""


def validate_login(data):
    """Return invalid field names, or an empty list if all fields are valid."""
    required_fields = ["app_id", "username", "password"]

    # JSON arrays, numbers, and null are not valid request objects.
    if not isinstance(data, dict):
        return required_fields

    invalid_fields = []
    for field in required_fields:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            invalid_fields.append(field)

    return invalid_fields


def validate_register(data):
    """Return invalid registration fields, or [] when input is valid."""
    invalid_fields = validate_login(data)

    # Require 12 characters and stay within bcrypt's 72-byte limit.
    if "password" not in invalid_fields:
        password = data["password"]
        if len(password) < 12 or len(password.encode("utf-8")) > 72:
            invalid_fields.append("password")

    return invalid_fields
