"""
Configuration management for OpenRoam.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class MqttConfig:
    """MQTT broker configuration."""

    host: str = "localhost"
    port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None
    client_id: str = "openroam-core"


@dataclass
class InfluxConfig:
    """InfluxDB configuration."""

    url: str = "http://localhost:8086"
    token: str = ""
    org: str = "openroam"
    bucket: str = "telemetry"


@dataclass
class HardwareConfig:
    """Hardware configuration."""

    i2c_bus: int = 1
    hats: list[str] = field(default_factory=list)


@dataclass
class ServerConfig:
    """API server configuration."""

    host: str = "0.0.0.0"
    port: int = 8080


@dataclass
class Config:
    """Complete OpenRoam configuration."""

    mqtt: MqttConfig = field(default_factory=MqttConfig)
    influx: InfluxConfig = field(default_factory=InfluxConfig)
    hardware: HardwareConfig = field(default_factory=HardwareConfig)
    server: ServerConfig = field(default_factory=ServerConfig)

    @classmethod
    def load(cls, path: Optional[str] = None) -> "Config":
        """Load configuration from file."""
        if path is None:
            # Look for config in standard locations
            locations = [
                Path("/etc/openroam/config.yaml"),
                Path.home() / ".config" / "openroam" / "config.yaml",
                Path("config.yaml"),
            ]
            for loc in locations:
                if loc.exists():
                    path = str(loc)
                    break

        config = cls()

        if path and Path(path).exists():
            with open(path) as f:
                data = yaml.safe_load(f)

            if data:
                if "mqtt" in data:
                    config.mqtt = MqttConfig(**data["mqtt"])
                if "influx" in data:
                    config.influx = InfluxConfig(**data["influx"])
                if "hardware" in data:
                    config.hardware = HardwareConfig(**data["hardware"])
                if "server" in data:
                    config.server = ServerConfig(**data["server"])

        # Override with environment variables
        config.mqtt.host = os.environ.get("MQTT_HOST", config.mqtt.host)
        config.mqtt.port = int(os.environ.get("MQTT_PORT", config.mqtt.port))
        config.influx.url = os.environ.get("INFLUX_URL", config.influx.url)
        config.influx.token = os.environ.get("INFLUX_TOKEN", config.influx.token)

        return config

    def save(self, path: str) -> None:
        """Save configuration to file."""
        from dataclasses import asdict

        data = {
            "mqtt": asdict(self.mqtt),
            "influx": asdict(self.influx),
            "hardware": asdict(self.hardware),
            "server": asdict(self.server),
        }

        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            yaml.safe_dump(data, f, default_flow_style=False)
