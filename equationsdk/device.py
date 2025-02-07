"""Device data model."""

from __future__ import annotations
from datetime import datetime

from equationsdk.utils import get_product_by_type_version

from . import utils
from .dto import EnergyConsumptionData
from .model import (
    ScheduleMode,
    EquationProduct,

    DEVICE_MODE_AUTO,

    DEVICE_PRESET_COMFORT,
    DEVICE_PRESET_ECO,
    DEVICE_PRESET_ICE,
    DEVICE_PRESET_OFF
)


class EquationDevice:
    """Represent a Equation device from the API."""

    id: str
    name: str
    serialnumber: str
    type: str

    # This represents the model of a particular product. Not the FW version.
    product_version: str

    firmware_version: str
    latest_firmware_version: str

    nominal_power: int
    power: bool

    # Describes the preset: ICE, ECO, Comfort, None
    preset: str
    mode: str

    temp: float
    temp_calc: float

    # Sensors
    temp_probe: float
    windows_open_status: bool

    # preset temperatures
    comfort_temp: float
    eco_temp: float
    ice_temp: float

    # User mode
    um_max_temp: float
    um_min_temp: float
    user_mode: bool
    ice_mode: bool

    # Schedule
    schedule: list[str]
    schedule_day: int
    schedule_hour: int

    energy_data: EnergyConsumptionData

    last_sync_datetime_app: datetime
    last_sync_datetime_device: datetime

    hass_available: bool

    def __init__(
        self,
        device_id: str,
        device_info: dict,
        energy_data: EnergyConsumptionData,
        latest_fw: str | None,
    ) -> None:
        """Initialize the device from the equation's json blob."""
        self.id = device_id
        self.type = device_info["data"]["type"]
        self.product_version = str.lower(device_info["data"]["product_version"])
        self.serialnumber = device_info["serialnumber"]
        self.update_data(device_info, energy_data, latest_fw)

    def update_data(
        self,
        device_info: dict,
        energy_data: EnergyConsumptionData,
        latest_fw: str | None,
    ) -> None:
        """Update the device data from a Json object."""

        data = device_info["data"]
        firmware_data = device_info.get("firmware")

        self.name = data["name"]
        self.nominal_power = int(data["nominal_power"])
        self.power = bool(data["power"])
        self.mode = data["mode"]

        self.temp_calc = float(data["temp_calc"])
        self.temp_probe = float(data["temp_probe"])

        self.windows_open_status = bool(data["windows_open_status"])

        self.comfort_temp = float(data["comfort"])
        self.eco_temp = float(data["eco"])
        self.ice_temp = float(data["ice"])

        # User mode settings are only valid for V2 radiators.
        if self.user_mode_supported():
            self.um_max_temp = float(data["um_max_temp"])
            self.um_min_temp = float(data["um_min_temp"])
            self.user_mode = bool(data["user_mode"])
        else:
            self.user_mode = False

        self.ice_mode = bool(data["ice_mode"])
        self.schedule = data["schedule"]

        self.preset = self.get_current_schedule_preset() if self.mode == DEVICE_MODE_AUTO else data["status"]
        self.temp = self.get_current_target_temp() if self.mode == DEVICE_MODE_AUTO else float(data["temp"])

        self.energy_data = energy_data

        self.last_sync_datetime_app = datetime.fromtimestamp(
            int(data["last_sync_datetime_app"]) / 1000.0
        )

        self.last_sync_datetime_device = datetime.fromtimestamp(
            int(data["last_sync_datetime_device"]) / 1000.0
        )

        if firmware_data:
            self.firmware_version = firmware_data.get("firmware_version_device")
        else:
            self.firmware_version = None

        self.latest_firmware_version = latest_fw
        self.hass_available = True

    def get_current_schedule_mode(self) -> ScheduleMode:
        """Return the current schedule mode for the device.

        Returns C for Comfort, E for Eco, O for no-schedule
        """
        day_time = utils.now()
        day_of_week = day_time.weekday()  # 0 is Monday
        hour_index = day_time.hour

        current_mode = self.schedule[day_of_week][hour_index]

        if current_mode == "C":
            return ScheduleMode.COMFORT
        elif current_mode == "E":
            return ScheduleMode.ECO
        
        return ScheduleMode.OFF

    def get_current_schedule_preset(self) -> ScheduleMode:
        """Return the current schedule preset for the device."""
        curr_mode = self.get_current_schedule_mode()

        if not self.power:
            return DEVICE_PRESET_OFF
        if curr_mode == ScheduleMode.COMFORT:
            return DEVICE_PRESET_COMFORT
        elif curr_mode == ScheduleMode.ECO:
            return DEVICE_PRESET_ECO
        elif self.ice_mode:
            return DEVICE_PRESET_ICE

        return DEVICE_PRESET_OFF

    def get_current_target_temp(self) -> float:
        """Return the current target temperature for the device."""
        curr_mode = self.get_current_schedule_mode()

        if not self.power:
            return 0.0
        elif curr_mode == ScheduleMode.COMFORT:
            return self.comfort_temp
        elif curr_mode == ScheduleMode.ECO:
            return self.eco_temp
        elif self.ice_mode:
            return self.ice_temp

        return 0.0

    def user_mode_supported(self) -> bool:
        """Return True if this device supports user mode."""
        return self.product_version == "v2"

    @property
    def equation_product(self) -> EquationProduct | None:
        """Return the product name."""
        return get_product_by_type_version(self.type, self.product_version)
