# Nav HAT

Primary navigation and sensor hub for OpenRoam.

**Estimated Cost:** ~$85 (buy path) / ~$45 (build path)

## Overview

The Nav HAT provides multi-constellation GPS positioning, 6-axis motion sensing, magnetic compass heading, and environmental monitoring. It serves as the sensor hub for the Nav Node.

## Features

- Multi-constellation GPS (GPS, GLONASS, Galileo, BeiDou)
- 6-axis IMU (accelerometer + gyroscope)
- Tilt-compensated digital compass
- Environmental sensors (temperature, humidity, pressure)
- Dead reckoning during GPS loss (tunnels, garages)
- 10Hz position update rate
- PPS output for time synchronization
- I2C sensor expansion bus

## Specifications

### GPS/GNSS
| Parameter | Value |
|-----------|-------|
| Receiver | Multi-constellation |
| Accuracy | 1.5m CEP |
| Update Rate | 10Hz |
| Time to First Fix | <30s cold, <1s hot |
| Antenna | Active ceramic patch (roof mount option) |

### IMU/Motion
| Parameter | Value |
|-----------|-------|
| Accelerometer Range | ±2g, ±4g, ±8g, ±16g |
| Gyroscope Range | ±125°/s to ±2000°/s |
| Sample Rate | Up to 32kHz |
| Resolution | 16-bit |

### Compass
| Parameter | Value |
|-----------|-------|
| Resolution | 18-bit |
| Range | ±8 Gauss |
| Accuracy | ±0.5° (after calibration) |

### Environmental
| Parameter | Value |
|-----------|-------|
| Temperature | -40°C to +85°C, ±0.5°C |
| Humidity | 0-100% RH, ±3% |
| Pressure | 300-1100 hPa, ±1 hPa |

---

## Option A: Buy Pre-Made Modules

The fastest path - use pre-assembled breakout boards.

### Components (Buy Path)

| Component | Description | Price | Source |
|-----------|-------------|-------|--------|
| u-blox MAX-M10S | GPS module | $18.50 | DigiKey 1909-MAX-M10S-ND |
| ICM-42688-P breakout | IMU | $12.00 | SparkFun or Adafruit |
| MMC5983MA breakout | Magnetometer | $10.00 | SparkFun or Adafruit |
| BME280 breakout | Environmental | $10.00 | Adafruit 2652 |
| STM32G071 Nucleo | Dev board | $15.00 | DigiKey 497-NUCLEO-G071RB-ND |
| GPS antenna | Active patch | $12.00 | u-blox or generic |
| Breakout carrier PCB | Custom board | $5.00 | JLCPCB |
| Headers/wiring | Misc | $3.00 | - |

**Buy Path Total: ~$85**

### Wiring (Buy Path)

```
                    ┌─────────────┐
                    │  STM32G071  │
                    │   (Nucleo)  │
                    └─────────────┘
                          │
        ┌────────┬────────┼────────┬────────┐
        │I2C     │I2C     │UART    │I2C     │
        ▼        ▼        ▼        ▼        │
   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
   │BME280  │ │ICM-42688│ │MAX-M10S│ │MMC5983 │
   │Breakout│ │Breakout │ │GPS     │ │Compass │
   └────────┘ └────────┘ └────────┘ └────────┘
```

All I2C devices share SDA/SCL bus. GPS uses UART for NMEA data.

---

## Option B: Build from Discrete Components

Full DIY for maximum learning and cost savings.

### Components (Build Path)

| Component | Description | Qty | Price | DigiKey PN |
|-----------|-------------|-----|-------|------------|
| MAX-M10S | GPS receiver IC | 1 | $18.50 | 1909-MAX-M10S-ND |
| ICM-42688-P | 6-axis IMU | 1 | $4.25 | 1428-ICM-42688-P-ND |
| MMC5983MA | Magnetometer | 1 | $3.50 | 1778-MMC5983MATR-ND |
| BME280 | Environmental | 1 | $4.95 | 828-BME280-ND |
| STM32G071RBT6 | MCU | 1 | $4.85 | 497-STM32G071RBT6-ND |
| 8MHz crystal | MCU clock | 1 | $0.50 | 535-9714-1-ND |
| 32.768kHz crystal | RTC | 1 | $0.50 | 535-9165-1-ND |
| LDO 3.3V | AMS1117-3.3 | 1 | $0.35 | LM1117MPX-3.3/NOPBCT-ND |
| Passive components | R, C, L | 1 set | $3.00 | - |
| SMA connector | GPS antenna | 1 | $1.50 | CONSMA001-ND |
| 40-pin header | Pi GPIO | 1 | $2.50 | S7122-ND |
| PCB | 2-layer | 1 | $2.00 | JLCPCB |

**Build Path Total: ~$45**

### Build from Scratch Options

#### GPS: Build Your Own Receiver (Advanced)

For the ultimate DIY experience, build a GPS receiver from first principles:

**Components:**
- MAX2769 GPS RF front-end ($15)
- TCXO 16.368MHz reference oscillator ($5)
- SAW filter 1575.42MHz ($3)
- LNA (low noise amplifier) - SPF5189Z ($3)
- FPGA or fast MCU for correlator (Lattice ICE40 ~$8)
- Patch antenna (build from PCB copper)

**Theory of Operation:**
1. Antenna receives L1 signal at 1575.42 MHz
2. LNA amplifies weak signal (~-130dBm)
3. SAW filter removes out-of-band interference
4. RF front-end downconverts to IF and digitizes
5. Correlator searches for satellite PRN codes
6. Position calculated from pseudoranges

**Resources:**
- Andrew Holme's homebrew GPS: http://www.aholme.co.uk/GPS/Main.htm
- GPS-SDR-SIM for testing
- GNSS-SDR open-source receiver software

#### IMU: Build from Discrete Sensors (Intermediate)

Build a 6-axis IMU from separate accelerometer and gyroscope:

**Accelerometer Options:**
- ADXL345 3-axis digital ($4)
- LIS3DH 3-axis digital ($3)
- Build analog with ADXL335 + ADC

**Gyroscope Options:**
- L3G4200D 3-axis digital ($5)
- ITG-3200 3-axis digital ($4)

**DIY Analog Accelerometer:**
- Use piezoelectric elements with charge amplifier
- Or MEMS die (salvage from broken phone)

#### Compass: Build a Fluxgate Magnetometer (Advanced)

Build a fluxgate magnetometer from scratch:

**Components:**
- Ferrite rod cores (2x)
- Copper wire for windings
- Excitation oscillator circuit
- Synchronous detector
- Op-amp signal conditioning

**Theory:**
1. Drive excitation coil at high frequency (~10kHz)
2. External field creates asymmetry in saturation
3. Sense coil detects second harmonic
4. Amplitude proportional to field strength

**Advantages:**
- Higher sensitivity than Hall effect
- Lower noise floor
- Educational value

---

## Schematic

See `kicad/nav-hat.kicad_sch` for complete schematic.

### Key Circuits

**GPS Power Filtering:**
```
5V ──┬── L1(10µH) ─┬── 3.3V_GPS
     │             │
    C1(100µF)    C2(100nF)
     │             │
    GND           GND
```

**I2C Bus with Level Shifting:**
```
3.3V ──┬── R1(4.7k) ── SDA
       │
      Q1(BSS138)
       │
5V ───┬── R2(4.7k) ── SDA_5V
```

---

## Firmware

### PlatformIO Configuration

```ini
[env:nav-hat]
platform = ststm32
board = nucleo_g071rb
framework = arduino
lib_deps =
    sparkfun/SparkFun u-blox GNSS Arduino Library@^2.0.0
    adafruit/Adafruit BME280 Library@^2.2.0
    adafruit/Adafruit ICM20X@^2.0.0
```

### Basic Example

```cpp
#include <Wire.h>
#include <SparkFun_u-blox_GNSS_Arduino_Library.h>
#include <Adafruit_BME280.h>

SFE_UBLOX_GNSS gps;
Adafruit_BME280 bme;

void setup() {
    Serial.begin(115200);
    Wire.begin();

    if (gps.begin()) {
        gps.setI2COutput(COM_TYPE_UBX);
        gps.setNavigationFrequency(10); // 10Hz
    }

    bme.begin(0x76);
}

void loop() {
    if (gps.getPVT()) {
        Serial.printf("Lat: %.6f, Lon: %.6f\n",
            gps.getLatitude() / 1e7,
            gps.getLongitude() / 1e7);
    }

    Serial.printf("Temp: %.1f°C, Humidity: %.1f%%\n",
        bme.readTemperature(),
        bme.readHumidity());

    delay(100);
}
```

---

## Integration with OpenRoam

### MQTT Topics

```
openroam/nav/gps/latitude      # Decimal degrees
openroam/nav/gps/longitude     # Decimal degrees
openroam/nav/gps/altitude      # Meters
openroam/nav/gps/speed         # m/s
openroam/nav/gps/heading       # Degrees
openroam/nav/gps/satellites    # Count
openroam/nav/imu/accel/x       # m/s²
openroam/nav/imu/accel/y
openroam/nav/imu/accel/z
openroam/nav/imu/gyro/x        # °/s
openroam/nav/imu/gyro/y
openroam/nav/imu/gyro/z
openroam/nav/compass/heading   # Degrees
openroam/nav/env/temperature   # °C
openroam/nav/env/humidity      # %
openroam/nav/env/pressure      # hPa
```

### RoamK Data Path

```json
{
  "vehicle": {
    "location": {
      "latitude": 35.123456,
      "longitude": -106.789012
    },
    "speed": 28.5,
    "heading": 225,
    "altitude": 1650
  },
  "environment": {
    "interior": {
      "temperature": 22.5,
      "humidity": 45
    }
  }
}
```

---

## Assembly

### Buy Path Assembly

1. Mount breakout boards to carrier PCB
2. Connect I2C bus (SDA, SCL, 3.3V, GND)
3. Connect GPS UART (TX, RX)
4. Attach GPS antenna to SMA connector
5. Stack on Raspberry Pi GPIO header
6. Flash firmware via USB

### Build Path Assembly

1. Solder SMD components (reflow or hot air)
2. Solder through-hole connectors
3. Test power rails with multimeter
4. Program STM32 via SWD
5. Calibrate compass (figure-8 motion)
6. Verify GPS acquisition outdoors

---

## Testing

### Functional Tests

```bash
# Check I2C devices
i2cdetect -y 1

# Read GPS NMEA
cat /dev/ttyS0

# Test IMU
python3 -c "import smbus2; print('IMU OK')"
```

### Expected I2C Addresses

| Device | Address |
|--------|---------|
| BME280 | 0x76 or 0x77 |
| ICM-42688 | 0x68 or 0x69 |
| MMC5983 | 0x30 |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No GPS fix | Check antenna connection, move outdoors |
| Compass drift | Recalibrate away from metal |
| IMU noise | Check decoupling capacitors |
| I2C errors | Check pull-up resistors, reduce speed |

---

## Resources

- [u-blox MAX-M10S datasheet](https://www.u-blox.com/en/product/max-m10-series)
- [ICM-42688-P datasheet](https://invensense.tdk.com/products/motion-tracking/6-axis/icm-42688-p/)
- [MMC5983MA datasheet](https://www.memsic.com/magnetometer)
- [BME280 datasheet](https://www.bosch-sensortec.com/products/environmental-sensors/humidity-sensors-bme280/)

## License

CERN-OHL-S-2.0
