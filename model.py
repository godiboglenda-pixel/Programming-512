
"""
models.py
Simple data models for CampusFlow.
A model describes the information used by the application.
"""
from dataclasses import dataclass


@dataclass
class User:
    id: int
    full_name: str
    username: str
    role: str
    campus: str


@dataclass
class Resource:
    id: int
    resource_code: str
    name: str
    category: str
    campus: str
    capacity: int
    notes: str = ""


@dataclass
class Booking:
    id: int
    resource_id: int
    user_id: int
    campus: str
    booking_date: str
    start_time: str
    duration: int
    purpose: str
    status: str
