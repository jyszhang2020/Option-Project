from datetime import (
    date,
    datetime,
)


def parse_date(date_str: str) -> datetime:
    """Parse data that's in format 'YYYY-MM-DD'"""
    year, month, day = date_str.split('-')
    return date(int(year), int(month), int(day))


def calculate_date_diff(date_one: datetime, date_two: datetime) -> int:
    """Return time difference between two dates"""
    return (date_two - date_one).days


def calculate_maturity_time(evaluation_date_str: str, expiration_date_str: str) -> float:
    """Calculates maturity time"""
    date_one: datetime = parse_date(evaluation_date_str)
    date_two: datetime = parse_date(expiration_date_str)
    date_diff = calculate_date_diff(date_one, date_two)
    return 0.000001 if date_diff == 0 else date_diff / 365.0
