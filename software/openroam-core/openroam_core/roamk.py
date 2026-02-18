"""
RoamK - OpenRoam Data Model

Similar to Signal K for marine vessels, RoamK provides a unified
data model for all vehicle systems.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Location:
    """GPS location data."""

    latitude: float = 0.0
    longitude: float = 0.0
    altitude: Optional[float] = None
    speed: Optional[float] = None
    heading: Optional[float] = None
    satellites: Optional[int] = None


@dataclass
class BatteryBank:
    """Battery bank state."""

    voltage: float = 0.0
    current: float = 0.0
    soc: float = 0.0
    temp: Optional[float] = None
    capacity_ah: Optional[float] = None


@dataclass
class PowerState:
    """Power system state."""

    house_battery: BatteryBank = field(default_factory=BatteryBank)
    chassis_battery: BatteryBank = field(default_factory=BatteryBank)
    solar_voltage: float = 0.0
    solar_current: float = 0.0
    solar_watts: float = 0.0
    solar_daily_wh: float = 0.0
    solar_lifetime_kwh: float = 0.0
    shore_connected: bool = False
    shore_voltage: float = 0.0
    shore_amps: float = 0.0
    alternator_charging: bool = False
    alternator_amps: float = 0.0


@dataclass
class TankLevel:
    """Tank level data."""

    level: float = 0.0
    gallons: Optional[float] = None
    capacity: Optional[float] = None


@dataclass
class TanksState:
    """All tank levels."""

    fresh: TankLevel = field(default_factory=TankLevel)
    grey: TankLevel = field(default_factory=TankLevel)
    black: TankLevel = field(default_factory=TankLevel)
    propane: TankLevel = field(default_factory=TankLevel)
    fuel: TankLevel = field(default_factory=TankLevel)


@dataclass
class ClimateZone:
    """Climate zone data."""

    temperature: float = 0.0
    setpoint: Optional[float] = None
    humidity: Optional[float] = None


@dataclass
class ClimateState:
    """Climate system state."""

    interior_temp: float = 0.0
    interior_humidity: float = 0.0
    exterior_temp: float = 0.0
    exterior_humidity: float = 0.0
    zones: dict[str, ClimateZone] = field(default_factory=dict)
    hvac_mode: str = "off"  # heat, cool, auto, off
    hvac_running: bool = False
    hvac_fan_speed: int = 0


@dataclass
class EngineState:
    """Engine/vehicle data from OBD-II."""

    rpm: int = 0
    coolant_temp: int = 0
    oil_temp: int = 0
    oil_pressure: int = 0
    trans_temp: int = 0
    throttle: int = 0
    load: int = 0
    fuel_rate: float = 0.0
    mpg_instant: float = 0.0
    mpg_average: float = 0.0
    dtc_codes: list[str] = field(default_factory=list)
    check_engine: bool = False


@dataclass
class SafetyState:
    """Safety system state."""

    smoke_status: str = "ok"  # ok, warning, alarm
    co_ppm: int = 0
    co_status: str = "ok"
    propane_ppm: int = 0
    propane_status: str = "ok"
    doors: dict[str, str] = field(default_factory=dict)  # door: open/closed
    alarm_armed: bool = False
    alarm_triggered: bool = False


@dataclass
class VehicleState:
    """Vehicle state."""

    location: Location = field(default_factory=Location)
    speed: float = 0.0
    heading: float = 0.0
    odometer: float = 0.0
    leveling_pitch: float = 0.0
    leveling_roll: float = 0.0
    leveling_state: str = "travel"  # leveling, level, travel


@dataclass
class MaintenanceItem:
    """Maintenance reminder."""

    service: str = ""
    due_miles: Optional[int] = None
    due_date: Optional[str] = None


@dataclass
class MaintenanceState:
    """Maintenance tracking."""

    oil_life: int = 100
    next_oil_miles: int = 5000
    tire_rotation_due: bool = False
    upcoming: list[MaintenanceItem] = field(default_factory=list)


@dataclass
class RoamKState:
    """Complete RoamK state."""

    vehicle: VehicleState = field(default_factory=VehicleState)
    power: PowerState = field(default_factory=PowerState)
    tanks: TanksState = field(default_factory=TanksState)
    climate: ClimateState = field(default_factory=ClimateState)
    engine: EngineState = field(default_factory=EngineState)
    safety: SafetyState = field(default_factory=SafetyState)
    maintenance: MaintenanceState = field(default_factory=MaintenanceState)
    last_update: datetime = field(default_factory=datetime.now)


class RoamK:
    """RoamK data store."""

    def __init__(self) -> None:
        self.state = RoamKState()
        self._callbacks: list[callable] = []

    def update_path(self, path: str, value: any) -> None:
        """Update a value at the given path."""
        parts = path.split(".")
        obj = self.state

        for part in parts[:-1]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return

        if hasattr(obj, parts[-1]):
            setattr(obj, parts[-1], value)
            self.state.last_update = datetime.now()
            self._notify()

    def get_path(self, path: str) -> any:
        """Get a value at the given path."""
        parts = path.split(".")
        obj = self.state

        for part in parts:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return None

        return obj

    def subscribe(self, callback: callable) -> None:
        """Subscribe to state changes."""
        self._callbacks.append(callback)

    def unsubscribe(self, callback: callable) -> None:
        """Unsubscribe from state changes."""
        self._callbacks.remove(callback)

    def _notify(self) -> None:
        """Notify all subscribers of state change."""
        for callback in self._callbacks:
            callback(self.state)

    def to_dict(self) -> dict:
        """Convert state to dictionary."""
        from dataclasses import asdict

        return asdict(self.state)
