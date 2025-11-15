from pydantic import BaseModel
from typing import List
from enum import Enum

# -----------------------------
# Damage type enumeration
# -----------------------------
class DamageType(str, Enum):
    broken_glass = "Broken glass"
    dent = "Dent"
    scratch = "Scratch"
    front_end_damage = "front-end-damage"
    rear_end_damage = "rear-end-damage"
    side_impact_damage = "side-impact-damage"
    other_damage = "other_damage"

# -----------------------------
# Represents a single detected damage
# -----------------------------
class Damage(BaseModel):
    type: DamageType                # Category of damage
    severity: int                   # 1-10 severity score derived from confidence
    confidence: float               # YOLO detection confidence
    coordinates: List[int]          # Bounding box [x1, y1, x2, y2]
    estimated_cost: int             # Cost estimate based on type & severity

# -----------------------------
# Complete comparison report
# -----------------------------
class CompareResponse(BaseModel):
    before_image: str               # Path or URL to before image
    after_image: str                # Path or URL to after image
    new_damages: List[Damage]       # List of new damages detected
    total_cost_estimate: int        # Sum of estimated costs
    summary: str                    # Human-readable summary
