"""Pydantic request and response models for the energy readings API."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReadingIn(BaseModel):
    """Payload for creating or fully replacing a reading."""

    reading_ts: datetime = Field(..., examples=["2016-05-27T18:10:00"])
    appliances_wh: int = Field(..., ge=0, examples=[60])
    lights_wh: int = Field(..., ge=0, examples=[30])


class ReadingUpdate(BaseModel):
    """Partial update payload. Only provided fields are changed."""

    reading_ts: Optional[datetime] = None
    appliances_wh: Optional[int] = Field(default=None, ge=0)
    lights_wh: Optional[int] = Field(default=None, ge=0)


class ReadingOut(ReadingIn):
    reading_id: int


class Message(BaseModel):
    detail: str
