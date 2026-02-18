"""
MQTT Client for OpenRoam

Handles connection to MQTT broker and message routing.
"""

import json
import logging
from typing import Callable, Optional

import paho.mqtt.client as mqtt

from .roamk import RoamK

logger = logging.getLogger(__name__)


# Topic to RoamK path mapping
TOPIC_MAP = {
    # Power
    "openroam/power/battery/house/voltage": "power.house_battery.voltage",
    "openroam/power/battery/house/current": "power.house_battery.current",
    "openroam/power/battery/house/soc": "power.house_battery.soc",
    "openroam/power/battery/house/temp": "power.house_battery.temp",
    "openroam/power/battery/chassis/voltage": "power.chassis_battery.voltage",
    "openroam/power/solar/watts": "power.solar_watts",
    "openroam/power/solar/daily_wh": "power.solar_daily_wh",
    "openroam/power/shore/connected": "power.shore_connected",
    "openroam/power/alternator/charging": "power.alternator_charging",
    # Tanks
    "openroam/tanks/fresh/level": "tanks.fresh.level",
    "openroam/tanks/grey/level": "tanks.grey.level",
    "openroam/tanks/black/level": "tanks.black.level",
    "openroam/tanks/propane/level": "tanks.propane.level",
    "openroam/tanks/fuel/level": "tanks.fuel.level",
    # Climate
    "openroam/climate/interior/temperature": "climate.interior_temp",
    "openroam/climate/interior/humidity": "climate.interior_humidity",
    "openroam/climate/exterior/temperature": "climate.exterior_temp",
    "openroam/climate/hvac/mode": "climate.hvac_mode",
    "openroam/climate/hvac/running": "climate.hvac_running",
    # Engine
    "openroam/engine/rpm": "engine.rpm",
    "openroam/engine/coolant_temp": "engine.coolant_temp",
    "openroam/engine/oil_temp": "engine.oil_temp",
    "openroam/engine/throttle": "engine.throttle",
    "openroam/engine/mpg_instant": "engine.mpg_instant",
    "openroam/engine/check_engine": "engine.check_engine",
    # Vehicle
    "openroam/nav/gps/latitude": "vehicle.location.latitude",
    "openroam/nav/gps/longitude": "vehicle.location.longitude",
    "openroam/nav/gps/speed": "vehicle.speed",
    "openroam/nav/gps/heading": "vehicle.heading",
    # Safety
    "openroam/safety/smoke/status": "safety.smoke_status",
    "openroam/safety/co/ppm": "safety.co_ppm",
    "openroam/safety/propane/ppm": "safety.propane_ppm",
}


class MqttClient:
    """MQTT client for OpenRoam."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 1883,
        client_id: str = "openroam-core",
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password

        self.client = mqtt.Client(
            client_id=client_id,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        )

        if username and password:
            self.client.username_pw_set(username, password)

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        self.roamk: Optional[RoamK] = None
        self.message_callbacks: list[Callable[[str, any], None]] = []
        self.connected = False

    def set_roamk(self, roamk: RoamK) -> None:
        """Set the RoamK data store."""
        self.roamk = roamk

    def add_message_callback(self, callback: Callable[[str, any], None]) -> None:
        """Add a callback for incoming messages."""
        self.message_callbacks.append(callback)

    def connect(self) -> None:
        """Connect to MQTT broker."""
        logger.info(f"Connecting to MQTT broker at {self.host}:{self.port}")
        self.client.connect(self.host, self.port)
        self.client.loop_start()

    def disconnect(self) -> None:
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic: str, payload: any, retain: bool = False) -> None:
        """Publish a message."""
        if isinstance(payload, (dict, list)):
            payload = json.dumps(payload)
        elif isinstance(payload, bool):
            payload = str(payload).lower()
        else:
            payload = str(payload)

        self.client.publish(topic, payload, retain=retain)

    def subscribe(self, topic: str) -> None:
        """Subscribe to a topic."""
        self.client.subscribe(topic)

    def _on_connect(
        self, client: mqtt.Client, userdata: any, flags: any, rc: int, properties: any = None
    ) -> None:
        """Handle connection."""
        if rc == 0:
            logger.info("Connected to MQTT broker")
            self.connected = True
            # Subscribe to all openroam topics
            self.client.subscribe("openroam/#")
        else:
            logger.error(f"Failed to connect to MQTT broker: {rc}")

    def _on_disconnect(
        self, client: mqtt.Client, userdata: any, rc: int, properties: any = None
    ) -> None:
        """Handle disconnection."""
        logger.warning(f"Disconnected from MQTT broker: {rc}")
        self.connected = False

    def _on_message(
        self, client: mqtt.Client, userdata: any, message: mqtt.MQTTMessage
    ) -> None:
        """Handle incoming message."""
        topic = message.topic
        payload = message.payload.decode("utf-8")

        # Parse payload
        value = self._parse_payload(payload)

        # Update RoamK if topic is mapped
        if self.roamk and topic in TOPIC_MAP:
            path = TOPIC_MAP[topic]
            self.roamk.update_path(path, value)

        # Call message callbacks
        for callback in self.message_callbacks:
            callback(topic, value)

    def _parse_payload(self, payload: str) -> any:
        """Parse MQTT payload."""
        # Try JSON
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            pass

        # Try number
        try:
            if "." in payload:
                return float(payload)
            return int(payload)
        except ValueError:
            pass

        # Try boolean
        if payload.lower() == "true":
            return True
        if payload.lower() == "false":
            return False

        # Return as string
        return payload
