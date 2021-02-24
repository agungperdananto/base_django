import re


def clean_str(value, lower=False, upper=False):
    if not value or not isinstance(value, str):
        return value

    value = re.sub(r'\s+', ' ', value).strip()
    if lower:
        value = value.lower()
    if upper:
        value = value.upper()
    return value
