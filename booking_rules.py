"""
booking_rules.py
Campus booking policies and validation are kept separate from the GUI/database.
This makes it easier to add a campus or adjust a rule later.
"""
from datetime import date, datetime, timedelta
from dataset import CAMPUS_POLICIES


def validate_booking(campus, booking_date, start_time, duration):
    """Raise ValueError with a readable message if a booking breaks a rule."""
    if campus not in CAMPUS_POLICIES:
        raise ValueError("Select a recognised campus.")

    policy = CAMPUS_POLICIES[campus]
    try:
        selected_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
        start = datetime.strptime(start_time, "%H:%M")
    except ValueError:
        raise ValueError(
            "Enter the date as YYYY-MM-DD and time as HH:MM (24-hour clock)."
        )

    if selected_date < date.today():
        raise ValueError("Bookings cannot be made for a date in the past.")

    if (
        not isinstance(duration, int)
        or duration < 1
        or duration > policy["max_hours"]
    ):
        raise ValueError(
            f"{campus} allows bookings from 1 to "
            f"{policy['max_hours']} hour(s)."
        )

    end_time = (start + timedelta(hours=duration)).strftime("%H:%M")
    start_text = start.strftime("%H:%M")

    if start_text < policy["start"] or end_time > policy["end"]:
        raise ValueError(
            f"Policy for {campus}: booking must fit between "
            f"{policy['start']} and {policy['end']}."
        )

    return True


def overlaps(start_time_a, duration_a, start_time_b, duration_b):
    """Return True if two time ranges overlap on the same date."""
    start_a = datetime.strptime(start_time_a, "%H:%M")
    start_b = datetime.strptime(start_time_b, "%H:%M")

    a1 = start_a.hour * 60 + start_a.minute
    b1 = start_b.hour * 60 + start_b.minute

    a2 = a1 + duration_a * 60
    b2 = b1 + duration_b * 60

    return a1 < b2 and b1 < a2
