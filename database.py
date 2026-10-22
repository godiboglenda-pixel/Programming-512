
"""
database.py
All SQLite operations are kept in this file.
The database file campusflow.db is created automatically in this folder.
"""

import sqlite3
import hashlib
import hmac
from datetime import datetime, date

from dataset import DEMO_USERS, SAMPLE_RESOURCES
from booking_rules import validate_booking, overlaps


DB_NAME = "campusflow.db"


def password_hash(password):
    """Hash passwords so plain-text passwords are not stored."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class Database:
    def __init__(self, filename=DB_NAME):
        self.connection = sqlite3.connect(filename)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()
        self.add_starter_data()

    def create_tables(self):
        self.connection.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            campus TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            campus TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            notes TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            campus TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            duration INTEGER NOT NULL,
            purpose TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active',
            created_at TEXT NOT NULL,
            FOREIGN KEY(resource_id) REFERENCES resources(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """)
        self.connection.commit()

    def add_starter_data(self):
        cursor = self.connection.cursor()

        for full_name, username, password, role, campus in DEMO_USERS:
            cursor.execute("""
                INSERT OR IGNORE INTO users
                (full_name, username, password_hash, role, campus)
                VALUES (?, ?, ?, ?, ?)
            """, (
                full_name,
                username,
                password_hash(password),
                role,
                campus
            ))

        for resource in SAMPLE_RESOURCES:
            cursor.execute("""
                INSERT OR IGNORE INTO resources
                (resource_code, name, category, campus, capacity, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, resource)

        self.connection.commit()

    def login(self, username, password):
        row = self.connection.execute(
            "SELECT * FROM users WHERE username=?",
            (username.strip(),)
        ).fetchone()

        if row and hmac.compare_digest(
            row["password_hash"],
            password_hash(password)
        ):
            return dict(row)

        return None

    def register_lecturer(
        self, full_name, username, password, campus
    ):
        if (
            not full_name.strip()
            or not username.strip()
            or len(password) < 6
        ):
            raise ValueError(
                "Enter your name and username, and use a password "
                "of at least 6 characters."
            )

        self.connection.execute("""
            INSERT INTO users
            (full_name, username, password_hash, role, campus)
            VALUES (?, ?, ?, 'Lecturer', ?)
        """, (
            full_name.strip(),
            username.strip(),
            password_hash(password),
            campus
        ))

        self.connection.commit()

    def get_resources(self, campus=None):
        if campus:
            return self.connection.execute(
                """
                SELECT * FROM resources
                WHERE campus=?
                ORDER BY category, name
                """,
                (campus,)
            ).fetchall()

        return self.connection.execute(
            """
            SELECT * FROM resources
            ORDER BY campus, category, name
            """
        ).fetchall()

    def add_resource(
        self, code, name, category, campus, capacity, notes=""
    ):
        if (
            not code.strip()
            or not name.strip()
            or int(capacity) < 1
        ):
            raise ValueError(
                "Enter a unique code, name and capacity greater than zero."
            )

        self.connection.execute("""
            INSERT INTO resources
            (resource_code, name, category, campus, capacity, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            code.strip().upper(),
            name.strip(),
            category,
            campus,
            int(capacity),
            notes.strip()
        ))

        self.connection.commit()

    def update_resource(
        self, resource_id, code, name, category,
        campus, capacity, notes=""
    ):
        if not code.strip() or not name.strip() or int(capacity) < 1:
            raise ValueError(
                "Enter a resource code, name and positive capacity."
            )

        self.connection.execute("""
            UPDATE resources
            SET resource_code=?, name=?, category=?, campus=?,
                capacity=?, notes=?
            WHERE id=?
        """, (
            code.strip().upper(),
            name.strip(),
            category,
            campus,
            int(capacity),
            notes.strip(),
            resource_id
        ))

        self.connection.commit()

    def delete_resource(self, resource_id):
        active = self.connection.execute(
            """
            SELECT COUNT(*) FROM bookings
            WHERE resource_id=? AND status='Active'
            """,
            (resource_id,)
        ).fetchone()[0]

        if active:
            raise ValueError(
                "This resource has active bookings. "
                "Cancel those bookings first."
            )

        self.connection.execute(
            "DELETE FROM resources WHERE id=?",
            (resource_id,)
        )
        self.connection.commit()

    def create_booking(
        self, resource_id, user_id, campus, booking_date,
        start_time, duration, purpose
    ):
        # Apply the rules for the selected campus.
        validate_booking(
            campus, booking_date, start_time, duration
        )

        resource = self.connection.execute(
            """
            SELECT * FROM resources
            WHERE id=? AND campus=?
            """,
            (resource_id, campus)
        ).fetchone()

        if not resource:
            raise ValueError(
                "Select a resource belonging to the active campus."
            )

        if not purpose.strip():
            raise ValueError("Enter the purpose of this booking.")

        # Check existing active bookings for the same resource and date.
        existing = self.connection.execute("""
            SELECT start_time, duration
            FROM bookings
            WHERE resource_id=?
              AND booking_date=?
              AND status='Active'
        """, (resource_id, booking_date)).fetchall()

        for item in existing:
            if overlaps(
                start_time,
                duration,
                item["start_time"],
                item["duration"]
            ):
                raise ValueError(
                    "That resource is already booked during "
                    "the selected time."
                )

        self.connection.execute("""
            INSERT INTO bookings
            (resource_id, user_id, campus, booking_date, start_time,
             duration, purpose, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Active', ?)
        """, (
            resource_id,
            user_id,
            campus,
            booking_date,
            start_time,
            duration,
            purpose.strip(),
            datetime.now().isoformat(timespec="seconds")
        ))

        self.connection.commit()

    def get_bookings(self, campus=None, user_id=None):
        sql = """
            SELECT b.*, r.resource_code,
                   r.name AS resource_name,
                   u.full_name, u.username
            FROM bookings b
            JOIN resources r ON r.id=b.resource_id
            JOIN users u ON u.id=b.user_id
        """

        filters = []
        values = []

        if campus:
            filters.append("b.campus=?")
            values.append(campus)

        if user_id is not None:
            filters.append("b.user_id=?")
            values.append(user_id)

        if filters:
            sql += " WHERE " + " AND ".join(filters)

        sql += """
            ORDER BY b.booking_date DESC, b.start_time DESC
        """

        return self.connection.execute(
            sql, values
        ).fetchall()

    def cancel_booking(self, booking_id, user_id=None):
        booking = self.connection.execute(
            "SELECT * FROM bookings WHERE id=?",
            (booking_id,)
        ).fetchone()

        if not booking:
            raise ValueError("Booking not found.")

        if user_id is not None and booking["user_id"] != user_id:
            raise ValueError("You can only cancel your own bookings.")

        if booking["status"] != "Active":
            raise ValueError("This booking is already cancelled.")

        if booking["booking_date"] < date.today().isoformat():
            raise ValueError("Past bookings cannot be cancelled.")

        self.connection.execute(
            """
            UPDATE bookings
            SET status='Cancelled'
            WHERE id=?
            """,
            (booking_id,)
        )

        self.connection.commit()

    def report_by_campus(self):
        return self.connection.execute("""
            SELECT campus,
                   COUNT(*) AS total,
                   ROUND(AVG(duration), 1) AS average_duration
            FROM bookings
            WHERE status='Active'
            GROUP BY campus
        """).fetchall()

    def resource_usage(self, campus=None):
        sql = """
            SELECT r.campus, r.resource_code, r.name,
                   COUNT(b.id) AS uses
            FROM resources r
            LEFT JOIN bookings b
                ON b.resource_id=r.id
                AND b.status='Active'
        """

        args = []

        if campus:
            sql += " WHERE r.campus=?"
            args.append(campus)

        sql += """
            GROUP BY r.id
            ORDER BY uses DESC, r.name
        """

        return self.connection.execute(
            sql, args
        ).fetchall()

    def close(self):
        self.connection.close()
