
"""
dataset.py
Starter data for the three campuses, campus booking rules, demo accounts,
and sample resources. Edit this file to change the starter dataset.
"""

# Three campuses supported by the system.
CAMPUSES = [
    "Braamfontein",
    "Durban",
    "Pretoria"
]


# Example booking policies for each campus.
# These are sample policies for the project, not official campus rules.
CAMPUS_POLICIES = {
    "Braamfontein": {
        "max_hours": 4,
        "start": "07:00",
        "end": "18:00",
        "description": (
            "Maximum 4 hours; bookings between 07:00 and 18:00"
        ),
    },

    "Durban": {
        "max_hours": 3,
        "start": "08:00",
        "end": "17:00",
        "description": (
            "Maximum 3 hours; bookings between 08:00 and 17:00"
        ),
    },

    "Pretoria": {
        "max_hours": 2,
        "start": "09:00",
        "end": "16:00",
        "description": (
            "Maximum 2 hours; bookings between 09:00 and 16:00"
        ),
    },
}


# Demo accounts for testing the application.
# Passwords are hashed before they are stored in SQLite.
DEMO_USERS = [
    (
        "Demo Lecturer",
        "lecturer",
        "Learn123!",
        "Lecturer",
        "Braamfontein"
    ),

    (
        "Braamfontein Admin",
        "admin",
        "Admin123!",
        "Campus Administrator",
        "Braamfontein"
    ),

    (
        "System Operator",
        "operator",
        "Operator123!",
        "System Operator",
        "Braamfontein"
    ),

    (
        "Durban Admin",
        "durbanadmin",
        "Admin123!",
        "Campus Administrator",
        "Durban"
    ),

    (
        "Pretoria Admin",
        "pretoriaadmin",
        "Admin123!",
        "Campus Administrator",
        "Pretoria"
    ),
]


# Sample resources registered at each campus.
# Each entry contains:
# resource code, name, category, campus, capacity, notes.
SAMPLE_RESOURCES = [
    (
        "BRA-LAB-01",
        "Innovation Computer Lab",
        "Computer Lab",
        "Braamfontein",
        30,
        "30 desktop computers"
    ),

    (
        "BRA-ROOM-02",
        "Ubuntu Seminar Room",
        "Seminar Room",
        "Braamfontein",
        24,
        "Projector included"
    ),

    (
        "BRA-PROJ-03",
        "Portable Projector A",
        "Projector",
        "Braamfontein",
        1,
        "HDMI connection"
    ),

    (
        "DBN-LAB-01",
        "Coastal Digital Lab",
        "Computer Lab",
        "Durban",
        25,
        "Student workstation lab"
    ),

    (
        "DBN-ROOM-02",
        "Oceanview Meeting Room",
        "Seminar Room",
        "Durban",
        16,
        "Whiteboard included"
    ),

    (
        "PTA-PROJ-01",
        "Smart Presentation Kit",
        "Presentation Equipment",
        "Pretoria",
        1,
        "Projector and clicker"
    ),

    (
        "PTA-ROOM-02",
        "Future Forum Room",
        "Seminar Room",
        "Pretoria",
        20,
        "Flexible seating"
    ),
]
