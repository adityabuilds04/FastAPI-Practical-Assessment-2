
from enum import Enum

from sqlmodel import SQLModel, Field


# -----------------------------
# EVENT STATUS
# -----------------------------

class EventStatus(str, Enum):
    Open = "Open"
    Closed = "Closed"


# -----------------------------
# EVENT MODEL
# -----------------------------

class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str
    venue: str
    capacity: int
    organizer: str
    status: EventStatus


# -----------------------------
# RESERVATION MODEL
# -----------------------------

class Reservation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    event_id: int
    student_name: str
    roll_number: str
    email: str
