import re


def validate_email(email):
    return bool(re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email.strip()))


def validate_password(password):
    return len(password) >= 6


def validate_positive_number(value):
    try:
        return float(value) >= 0
    except (TypeError, ValueError):
        return False


def validate_year(value):
    try:
        year = int(value)
        return 1990 <= year <= 2035
    except (TypeError, ValueError):
        return False


def validate_seating(value):
    try:
        seats = int(value)
        return seats > 0
    except (TypeError, ValueError):
        return False
