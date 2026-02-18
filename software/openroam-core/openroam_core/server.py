"""
OpenRoam API Server

FastAPI server providing REST API for the dashboard and external integrations.
"""

import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Config
from .mqtt_client import MqttClient
from .roamk import RoamK

logger = logging.getLogger(__name__)

# Global instances
config: Config
roamk: RoamK
mqtt_client: MqttClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global config, roamk, mqtt_client

    # Load configuration
    config = Config.load()

    # Initialize RoamK data store
    roamk = RoamK()

    # Initialize MQTT client
    mqtt_client = MqttClient(
        host=config.mqtt.host,
        port=config.mqtt.port,
        client_id=config.mqtt.client_id,
        username=config.mqtt.username,
        password=config.mqtt.password,
    )
    mqtt_client.set_roamk(roamk)
    mqtt_client.connect()

    logger.info("OpenRoam server started")

    yield

    # Cleanup
    mqtt_client.disconnect()
    logger.info("OpenRoam server stopped")


app = FastAPI(
    title="OpenRoam API",
    description="REST API for OpenRoam mobile living computing platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"name": "OpenRoam API", "version": "0.1.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "mqtt_connected": mqtt_client.connected if mqtt_client else False,
    }


@app.get("/state")
async def get_state():
    """Get complete RoamK state."""
    return roamk.to_dict()


@app.get("/state/{path:path}")
async def get_state_path(path: str):
    """Get state at specific path."""
    # Convert URL path to dot notation
    path = path.replace("/", ".")
    value = roamk.get_path(path)
    if value is None:
        return {"error": "Path not found"}
    return {"path": path, "value": value}


@app.post("/command/{topic:path}")
async def send_command(topic: str, payload: dict):
    """Send MQTT command."""
    full_topic = f"openroam/{topic}"
    mqtt_client.publish(full_topic, payload.get("value", ""))
    return {"status": "sent", "topic": full_topic}


# Power endpoints
@app.get("/power")
async def get_power():
    """Get power state."""
    from dataclasses import asdict

    return asdict(roamk.state.power)


@app.get("/power/batteries")
async def get_batteries():
    """Get battery states."""
    from dataclasses import asdict

    return {
        "house": asdict(roamk.state.power.house_battery),
        "chassis": asdict(roamk.state.power.chassis_battery),
    }


# Tanks endpoints
@app.get("/tanks")
async def get_tanks():
    """Get tank levels."""
    from dataclasses import asdict

    return asdict(roamk.state.tanks)


# Climate endpoints
@app.get("/climate")
async def get_climate():
    """Get climate state."""
    from dataclasses import asdict

    return asdict(roamk.state.climate)


@app.post("/climate/hvac/mode")
async def set_hvac_mode(mode: str):
    """Set HVAC mode."""
    mqtt_client.publish("openroam/climate/hvac/mode/set", mode)
    return {"status": "sent", "mode": mode}


@app.post("/climate/hvac/setpoint")
async def set_temperature(temp: float):
    """Set temperature setpoint."""
    mqtt_client.publish("openroam/climate/hvac/setpoint/set", temp)
    return {"status": "sent", "setpoint": temp}


# Vehicle endpoints
@app.get("/vehicle")
async def get_vehicle():
    """Get vehicle state."""
    from dataclasses import asdict

    return asdict(roamk.state.vehicle)


@app.get("/vehicle/location")
async def get_location():
    """Get current location."""
    from dataclasses import asdict

    return asdict(roamk.state.vehicle.location)


# Engine endpoints
@app.get("/engine")
async def get_engine():
    """Get engine state."""
    from dataclasses import asdict

    return asdict(roamk.state.engine)


# Safety endpoints
@app.get("/safety")
async def get_safety():
    """Get safety state."""
    from dataclasses import asdict

    return asdict(roamk.state.safety)


# Maintenance endpoints
@app.get("/maintenance")
async def get_maintenance():
    """Get maintenance state."""
    from dataclasses import asdict

    return asdict(roamk.state.maintenance)


def main():
    """Main entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    config = Config.load()

    uvicorn.run(
        "openroam_core.server:app",
        host=config.server.host,
        port=config.server.port,
        reload=False,
    )


if __name__ == "__main__":
    main()
