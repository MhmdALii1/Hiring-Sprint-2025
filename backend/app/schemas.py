# backend/app/schemas.py
"""
Pydantic models for request/response payloads used by the VCA API.
Severity is an integer 1..10. Cost estimates are integer USD approximations.
"""
from pydantic import BaseModel
from typing import List


class Damage(BaseModel):
    """
    Represents a detected damage item.
    - type: damage category label (demo mapping)
    - severity: integer 1..10
    - cost_estimate: integer USD
    - coordinates: bounding box [x1, y1, x2, y2]
    """
    type: str
    severity: int
    cost_estimate: int
    coordinates: List[int]


class CompareResponse(BaseModel):
    """
    Response when comparing before/after images.
    - session_id: generated session identifier for this inspection
    - before_image, after_image: saved file paths (temporary)
    - new_damages: list of Damage items found in the after image
    - total_cost_estimate: integer USD total for new damages
    - summary: short human-readable summary
    """
    session_id: str
    before_image: str
    after_image: str
    new_damages: List[Damage]
    total_cost_estimate: int
    summary: str


class ImageUploadResponse(BaseModel):
    """Generic response for an upload operation."""
    filename: str
    message: str
