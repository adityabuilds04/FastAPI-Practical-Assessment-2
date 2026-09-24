
from pydantic import BaseModel, EmailStr, Field, field_validator

from models import EventStatus


# -----------------------------
# EVENT CREATE
# -----------------------------

class EventCreate(BaseModel):
    title: str = Field(min_length=1)
    venue: str = Field(min_length=1)
    capacity: int = Field(gt=0)
    organizer: str = Field(min_length=1)
    status: EventStatus

    @field_validator("title", "venue", "organizer")
    @classmethod
    def validate_text(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value


# -----------------------------
# EVENT UPDATE
# -----------------------------

class EventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    venue: str | None = Field(default=None, min_length=1)
    capacity: int | None = Field(default=None, gt=0)
    organizer: str | None = Field(default=None, min_length=1)
    status: EventStatus | None = None

    @field_validator("title", "venue", "organizer")
    @classmethod
    def validate_text(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Field cannot be empty")
        return value


# -----------------------------
# RESERVATION CREATE
# -----------------------------

class ReservationCreate(BaseModel):
    student_name: str = Field(min_length=1)
    roll_number: str = Field(min_length=1)
    email: EmailStr

    @field_validator("student_name", "roll_number")
    @classmethod
    def validate_text(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value
