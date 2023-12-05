"""Data Model enumerations."""

from __future__ import annotations
from enum import Enum


class EquationProduct(Enum):
    """Device Models and Versions enum"""

    def __init__(self, product_name: str, device_type: str, version: str):
        """Initializes the enum."""
        self.product_name = product_name
        self.device_type = device_type
        self.version = version

    RADIATOR_V2 = "Equation HERA", "radiator", "v2"

DEVICE_MODE_AUTO = "auto"
DEVICE_MODE_MANUAL = "manual"

DEVICE_PRESET_COMFORT = "comfort"
DEVICE_PRESET_ECO = "eco"
DEVICE_PRESET_OFF = "off"

class ScheduleMode(Enum):
    """Radiator schedule modes."""

    COMFORT = "C"
    ECO = "E"
    OFF = "O"
