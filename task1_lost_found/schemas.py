
from pydantic import BaseModel, Field, field_validator
from models import ItemStatus


class ItemCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=5)
    category: str = Field(min_length=1)
    location: str = Field(min_length=1)
    reported_by: str = Field(min_length=1)
    status: ItemStatus

    @field_validator(
        "title",
        "description",
        "category",
        "location",
        "reported_by"
    )
    @classmethod
    def validate_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value


class ItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=5)
    category: str | None = Field(default=None, min_length=1)
    location: str | None = Field(default=None, min_length=1)
    reported_by: str | None = Field(default=None, min_length=1)
    status: ItemStatus | None = None

    @field_validator(
        "title",
        "description",
        "category",
        "location",
        "reported_by"
    )
    @classmethod
    def validate_not_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Field cannot be empty")
        return value