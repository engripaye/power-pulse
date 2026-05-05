def is_valid_phone_number(value: str) -> bool:
    return value.startswith("+") and len(value) >= 10

