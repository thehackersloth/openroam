"""
Mock Data Generator

Generates simulated sensor data for development and testing
without actual hardware.
"""

import logging
import math
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

from .config import Config

logger = logging.getLogger(__name__)


class MockDataGenerator:
    """Generate mock sensor data for testing."""

    def __init__(self, mqtt_host: str = "localhost", mqtt_port: int = 1883) -> None:
        self.client = mqtt.Client(
            client_id="openroam-mock",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        )
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port

        # State for realistic simulation
        self.time_offset = 0
        self.house_soc = 85.0
        self.solar_base = 0.0
        self.location = {"lat": 35.0853, "lon": -106.6056}  # Albuquerque
        self.speed = 0.0
        self.heading = 0.0
        self.engine_running = False

    def connect(self) -> None:
        """Connect to MQTT broker."""
        self.client.connect(self.mqtt_host, self.mqtt_port)
        self.client.loop_start()
        logger.info(f"Connected to MQTT at {self.mqtt_host}:{self.mqtt_port}")

    def disconnect(self) -> None:
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic: str, value) -> None:
        """Publish a value to MQTT."""
        self.client.publish(topic, str(value))

    def generate_power_data(self) -> None:
        """Generate power system data."""
        # Simulate solar based on time of day
        hour = (datetime.now().hour + self.time_offset) % 24
        if 6 <= hour <= 18:
            # Daylight hours - sine curve peaking at noon
            solar_factor = math.sin((hour - 6) * math.pi / 12)
            self.solar_base = 400 * solar_factor + random.uniform(-20, 20)
        else:
            self.solar_base = 0

        solar_watts = max(0, self.solar_base)
        solar_voltage = 35.0 + random.uniform(-2, 2) if solar_watts > 0 else 0
        solar_current = solar_watts / solar_voltage if solar_voltage > 0 else 0

        # House battery - discharge at night, charge during day
        load = random.uniform(50, 150)  # Base load in watts
        net_power = solar_watts - load

        # SOC changes based on net power
        self.house_soc += net_power * 0.0001  # Very slow change
        self.house_soc = max(20, min(100, self.house_soc))

        house_voltage = 12.0 + (self.house_soc - 50) * 0.04 + random.uniform(-0.1, 0.1)
        house_current = net_power / house_voltage

        self.publish("openroam/power/battery/house/voltage", f"{house_voltage:.2f}")
        self.publish("openroam/power/battery/house/current", f"{house_current:.1f}")
        self.publish("openroam/power/battery/house/soc", f"{self.house_soc:.0f}")
        self.publish("openroam/power/battery/house/temp", f"{75 + random.uniform(-5, 5):.0f}")

        self.publish("openroam/power/battery/chassis/voltage", f"{12.6 + random.uniform(-0.2, 0.2):.2f}")
        self.publish("openroam/power/battery/chassis/soc", "100")

        self.publish("openroam/power/solar/voltage", f"{solar_voltage:.1f}")
        self.publish("openroam/power/solar/current", f"{solar_current:.1f}")
        self.publish("openroam/power/solar/watts", f"{solar_watts:.0f}")
        self.publish("openroam/power/solar/daily_wh", f"{solar_watts * 2:.0f}")

        self.publish("openroam/power/shore/connected", "false")
        self.publish("openroam/power/alternator/charging", "true" if self.engine_running else "false")
        if self.engine_running:
            self.publish("openroam/power/alternator/amps", f"{45 + random.uniform(-5, 5):.0f}")

    def generate_tank_data(self) -> None:
        """Generate tank level data."""
        # Slowly decreasing fresh water, slowly increasing waste
        fresh = 65 + random.uniform(-2, 2)
        grey = 35 + random.uniform(-2, 2)
        black = 20 + random.uniform(-2, 2)
        propane = 55 + random.uniform(-1, 1)
        fuel = 45 + random.uniform(-1, 1)

        self.publish("openroam/tanks/fresh/level", f"{fresh:.0f}")
        self.publish("openroam/tanks/fresh/gallons", f"{fresh * 0.4:.1f}")
        self.publish("openroam/tanks/grey/level", f"{grey:.0f}")
        self.publish("openroam/tanks/black/level", f"{black:.0f}")
        self.publish("openroam/tanks/propane/level", f"{propane:.0f}")
        self.publish("openroam/tanks/fuel/level", f"{fuel:.0f}")
        self.publish("openroam/tanks/fuel/range_miles", f"{fuel * 5:.0f}")

    def generate_climate_data(self) -> None:
        """Generate climate data."""
        hour = datetime.now().hour
        # Simulate temperature variation
        base_exterior = 70 + 15 * math.sin((hour - 6) * math.pi / 12)
        exterior_temp = base_exterior + random.uniform(-2, 2)

        # Interior tries to maintain ~72F
        interior_temp = 72 + random.uniform(-2, 2)
        interior_humidity = 45 + random.uniform(-5, 5)

        self.publish("openroam/climate/interior/temperature", f"{interior_temp:.1f}")
        self.publish("openroam/climate/interior/humidity", f"{interior_humidity:.0f}")
        self.publish("openroam/climate/exterior/temperature", f"{exterior_temp:.1f}")
        self.publish("openroam/climate/hvac/mode", "auto")
        self.publish("openroam/climate/hvac/running", "true" if abs(interior_temp - 72) > 3 else "false")

    def generate_vehicle_data(self) -> None:
        """Generate vehicle/GPS data."""
        # Simulate slow movement
        if random.random() > 0.95:
            self.speed = random.uniform(0, 65)
            self.heading = random.uniform(0, 360)

        # Update location based on speed/heading
        if self.speed > 0:
            # Very simplified movement
            self.location["lat"] += math.cos(math.radians(self.heading)) * self.speed * 0.00001
            self.location["lon"] += math.sin(math.radians(self.heading)) * self.speed * 0.00001

        self.publish("openroam/nav/gps/latitude", f"{self.location['lat']:.6f}")
        self.publish("openroam/nav/gps/longitude", f"{self.location['lon']:.6f}")
        self.publish("openroam/nav/gps/speed", f"{self.speed:.1f}")
        self.publish("openroam/nav/gps/heading", f"{self.heading:.0f}")
        self.publish("openroam/nav/gps/altitude", f"{1500 + random.uniform(-10, 10):.0f}")
        self.publish("openroam/nav/gps/satellites", f"{random.randint(8, 12)}")

    def generate_engine_data(self) -> None:
        """Generate engine/OBD data."""
        self.engine_running = self.speed > 0

        if self.engine_running:
            rpm = 1000 + self.speed * 30 + random.uniform(-100, 100)
            coolant = 195 + random.uniform(-5, 5)
            oil_temp = 210 + random.uniform(-10, 10)
            throttle = min(100, self.speed * 1.5 + random.uniform(-5, 5))
            mpg = 10 + random.uniform(-2, 2) if self.speed > 10 else 0
        else:
            rpm = 0
            coolant = 75 + random.uniform(-5, 5)
            oil_temp = 75 + random.uniform(-5, 5)
            throttle = 0
            mpg = 0

        self.publish("openroam/engine/rpm", f"{rpm:.0f}")
        self.publish("openroam/engine/coolant_temp", f"{coolant:.0f}")
        self.publish("openroam/engine/oil_temp", f"{oil_temp:.0f}")
        self.publish("openroam/engine/oil_pressure", f"{45 + random.uniform(-5, 5):.0f}")
        self.publish("openroam/engine/throttle", f"{throttle:.0f}")
        self.publish("openroam/engine/load", f"{throttle * 0.7:.0f}")
        self.publish("openroam/engine/mpg_instant", f"{mpg:.1f}")
        self.publish("openroam/engine/mpg_average", "10.2")
        self.publish("openroam/engine/check_engine", "false")

    def generate_safety_data(self) -> None:
        """Generate safety system data."""
        self.publish("openroam/safety/smoke/status", "ok")
        self.publish("openroam/safety/co/ppm", "0")
        self.publish("openroam/safety/co/status", "ok")
        self.publish("openroam/safety/propane/ppm", "0")
        self.publish("openroam/safety/propane/status", "ok")
        self.publish("openroam/safety/alarm/armed", "false")

    def run(self, interval: float = 1.0) -> None:
        """Run the mock data generator."""
        logger.info("Starting mock data generation...")
        try:
            while True:
                self.generate_power_data()
                self.generate_tank_data()
                self.generate_climate_data()
                self.generate_vehicle_data()
                self.generate_engine_data()
                self.generate_safety_data()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Stopping mock data generation")


def main() -> None:
    """Main entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    config = Config.load()
    generator = MockDataGenerator(config.mqtt.host, config.mqtt.port)
    generator.connect()

    try:
        generator.run()
    finally:
        generator.disconnect()


if __name__ == "__main__":
    main()
