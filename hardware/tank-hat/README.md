# Tank HAT

Water, fuel, and propane tank monitoring for OpenRoam.

**Estimated Cost:** ~$55 (buy path) / ~$30 (build path)

## Overview

The Tank HAT monitors up to 6 tank levels using resistive, capacitive, ultrasonic, or pressure sensors. Compatible with standard RV tank sensors and aftermarket systems like SeeLevel and Garnet.

## Features

- 6 tank input channels
- Resistive sensors (0-240Ω, 10-180Ω RV standard)
- Capacitive sensors (PWM input)
- Ultrasonic sensors (serial input)
- Pressure sensors (4-20mA)
- Propane remote sender compatible
- Wireless sensor support (ESP32 WiFi)
- Auto-calibration mode
- Pump control output

## Specifications

### Tank Inputs
| Channel | Sensor Types | Range |
|---------|-------------|-------|
| 1-4 | Resistive/Capacitive | 0-500Ω or PWM |
| 5 | Pressure/Ultrasonic | 4-20mA or Serial |
| 6 | Propane sender | 0-90Ω |

### Supported Tanks
- Fresh water (primary + secondary)
- Grey water
- Black water
- Propane (LPG)
- Fuel (diesel/gas)
- DEF fluid

---

## Option A: Buy Pre-Made Modules

### Components (Buy Path)

| Component | Description | Qty | Price | Source |
|-----------|-------------|-----|-------|--------|
| ADS1115 breakout | 16-bit ADC | 2 | $6.00 | Adafruit 1085 |
| ESP32-S3 DevKit | WiFi MCU | 1 | $10.00 | Various |
| 4-20mA receiver | Current loop | 2 | $5.00 | Amazon |
| Precision resistors | 0.1% kit | 1 | $8.00 | Amazon |
| Screw terminals | Tank inputs | 6 | $3.00 | DigiKey |
| TVS protection | ESD | 1 | $3.00 | DigiKey |
| Carrier PCB | Custom | 1 | $5.00 | JLCPCB |

**Buy Path Total: ~$55**

---

## Option B: Build from Discrete Components

### Components (Build Path)

| Component | Description | Qty | Price | DigiKey PN |
|-----------|-------------|-----|-------|------------|
| ADS1115IDGSR | 16-bit ADC | 2 | $4.25 | 296-ADS1115IDGSR-ND |
| ESP32-S3-WROOM | WiFi module | 1 | $3.50 | 1965-ESP32-S3-WROOM-1-N4-ND |
| Precision resistors | 0.1% 1k, 4.7k | 12 | $0.15 | Various |
| TVS array | SM712 | 1 | $0.50 | SM712-TPCT-ND |
| 250Ω resistor | 4-20mA sense | 2 | $0.20 | High precision |
| Op-amp | MCP6002 | 1 | $0.75 | MCP6002-I/P-ND |
| Passives | R, C | 1 set | $2.00 | - |
| PCB | 2-layer | 1 | $2.00 | JLCPCB |

**Build Path Total: ~$30**

### Build from Scratch Options

#### Capacitive Tank Sensor: Build Your Own (Intermediate)

Build a capacitive level sensor from raw materials:

**Components:**
- Aluminum tape or copper strips (electrodes)
- Coaxial cable or shielded wire
- 555 timer or dedicated capacitance-to-digital IC
- Reference capacitor

**Theory of Operation:**
```
                    ┌─────────────────┐
Water Level →       │░░░░░░░░░░░░░░░░░│  ← Inner electrode
                    │                 │
                    │    Tank Wall    │  ← Dielectric
                    │                 │
                    │░░░░░░░░░░░░░░░░░│  ← Outer electrode
                    └─────────────────┘

Capacitance = ε₀ × εᵣ × A / d

Where:
- εᵣ(air) ≈ 1.0
- εᵣ(water) ≈ 80
- As water level rises, total capacitance increases
```

**555 Timer Capacitance Measurement:**
```
         ┌────────────────────┐
         │                    │
    VCC ─┤8     555     3├─── Output (frequency)
         │      Timer       │
         │                    │
  Discharge─┤7           2├─┬── Sensor
         │                    │  │
    Threshold─┤6               │  │
         │                    │  │
    GND ─┤1              │  │
         └────────────────────┘  │
                                 │
                            C_ref + C_sensor

Frequency = 1.44 / ((R1 + 2×R2) × C_total)
```

**Dedicated IC Option:**
- FDC1004 capacitance-to-digital ($3)
- LDC1614 inductive-to-digital (for metal tanks)

#### Ultrasonic Tank Sensor: Build Your Own (Basic)

Build an ultrasonic distance sensor:

**Components:**
- HC-SR04 ultrasonic module ($2)
- Or build from discrete:
  - 40kHz ultrasonic transducer pair
  - LM567 tone decoder
  - 555 timer for transmit pulse
  - Op-amp for receive amplification

**DIY Ultrasonic Circuit:**
```
        Transmit                    Receive
        ┌──────┐                    ┌──────┐
Trigger ┤ 555  ├─── 40kHz burst ───► Tank ────┤ Amp  ├─── Echo
        │Timer │                    (reflect) │LM358 │
        └──────┘                              └──────┘
                                                 │
                                                 ▼
                                            ┌──────┐
                                            │LM567 │─── Distance
                                            │Decode│
                                            └──────┘

Distance = (Time × Speed_of_sound) / 2
         = (Time_µs × 343) / 2000 mm
```

**Advantages of DIY:**
- Customize for tank geometry
- Higher accuracy with averaging
- Temperature compensation

#### Resistive Sensor Interface: Build Precision Divider (Basic)

Build precision resistance measurement:

```
                 VCC (3.3V)
                    │
                    │
                R_ref (1kΩ 0.1%)
                    │
                    ├───────── To ADC
                    │
                R_sensor (tank)
                    │
                   GND

R_sensor = R_ref × (V_adc / (VCC - V_adc))

For 10-180Ω RV sensor:
- Use 220Ω reference
- Gives 0.15V - 1.75V range
```

**Multi-Point Calibration:**
```python
# Calibration table (measured resistance → level %)
calibration = {
    10: 0,     # Empty
    40: 25,
    90: 50,
    140: 75,
    180: 100   # Full
}

def resistance_to_level(r):
    # Linear interpolation between points
    for i, (r1, l1) in enumerate(calibration.items()):
        if i < len(calibration) - 1:
            r2, l2 = list(calibration.items())[i+1]
            if r1 <= r <= r2:
                return l1 + (r - r1) * (l2 - l1) / (r2 - r1)
    return 0
```

#### Wireless Tank Sensors: Build ESP-NOW Network (Advanced)

Build battery-powered wireless sensors:

**Sensor Node (per tank):**
```
Components:
- ESP32-C3 module ($3)
- ADS1015 12-bit ADC ($2)
- LiFePO4 battery AA ($5)
- Solar cell 5V/100mA ($3)
- TP4056 charger ($0.50)
- Tank sensor

Power Budget:
- Sleep: 10µA
- Wake + TX: 100mA for 50ms
- 10 readings/hour = 0.014mAh
- AA battery (2500mAh) = years of operation
```

**ESP-NOW Protocol:**
```cpp
// Sensor node
#include <esp_now.h>

struct TankData {
    uint8_t tank_id;
    uint16_t level_raw;
    uint16_t battery_mv;
};

void setup() {
    esp_now_init();
    esp_now_add_peer(&gateway_addr);
}

void loop() {
    TankData data = readSensors();
    esp_now_send(gateway_addr, (uint8_t*)&data, sizeof(data));
    esp_deep_sleep(360e6); // 6 minutes
}
```

---

## Wiring Guide

### Standard RV Resistive Sensors

```
                    Tank HAT
    ┌────────────────────────────────┐
    │  CH1   CH2   CH3   CH4        │
    │   │     │     │     │         │
    │   │     │     │     │         │
    └───┼─────┼─────┼─────┼─────────┘
        │     │     │     │
        │     │     │     │
      Fresh  Grey  Black Fuel
      Water  Water Water Tank
        │     │     │     │
        └──┬──┘     └──┬──┘
           │           │
          GND        GND (chassis)
```

### SeeLevel Compatibility

SeeLevel uses capacitive strips. Connect to PWM inputs or use adapter:

```
SeeLevel     Tank HAT Adapter
┌────────┐   ┌────────────────┐
│Signal  ├───┤ PWM Input      │
│GND     ├───┤ GND            │
│+12V    ├───┤ +12V           │
└────────┘   └────────────────┘
```

### Propane Remote Sender

```
Propane Tank               Tank HAT
┌──────────────┐           ┌──────────┐
│ Sender       │           │  CH6     │
│  Signal (S) ─┼───────────┤  PROP+   │
│  Ground (G) ─┼───────────┤  PROP-   │
└──────────────┘           └──────────┘

Standard propane senders: 0Ω (full) to 90Ω (empty)
```

---

## Firmware

### Tank Reading Algorithm

```cpp
class TankSensor {
    ADS1115 adc;
    float calibration[6][5]; // 5-point calibration per tank

public:
    float readLevel(uint8_t channel) {
        int16_t raw = adc.readADC_SingleEnded(channel);

        // Convert to resistance
        float voltage = raw * 0.1875 / 1000.0; // mV to V
        float resistance = REF_RESISTOR * voltage / (VCC - voltage);

        // Apply calibration curve
        return interpolate(calibration[channel], resistance);
    }

    void calibrate(uint8_t channel, float level) {
        // Store current reading as calibration point
        int16_t raw = adc.readADC_SingleEnded(channel);
        float resistance = rawToResistance(raw);

        // Find nearest calibration slot
        int slot = (int)(level / 25); // 0, 25, 50, 75, 100
        calibration[channel][slot] = resistance;

        saveCalibration();
    }
};
```

### Pump Control

```cpp
#define PUMP_PIN 25
#define FRESH_TANK_CH 0

void checkPumpControl() {
    float freshLevel = tanks.readLevel(FRESH_TANK_CH);

    // Auto-shutoff when tank empty
    if (freshLevel < 5.0) {
        digitalWrite(PUMP_PIN, LOW);
        mqtt.publish("openroam/tanks/pump/warning", "LOW_WATER");
    }
}
```

---

## Integration

### MQTT Topics

```
openroam/tanks/fresh/level         # %
openroam/tanks/fresh/gallons       # Calculated from tank size
openroam/tanks/grey/level
openroam/tanks/grey/gallons
openroam/tanks/black/level
openroam/tanks/black/gallons
openroam/tanks/propane/level
openroam/tanks/propane/pounds
openroam/tanks/fuel/level
openroam/tanks/fuel/gallons
openroam/tanks/fuel/range_miles    # Calculated from MPG
openroam/tanks/pump/state          # on/off
openroam/tanks/pump/command        # on/off
```

### RoamK Data

```json
{
  "tanks": {
    "fresh": {
      "level": 75,
      "gallons": 30,
      "capacity": 40
    },
    "grey": {
      "level": 40,
      "gallons": 16
    },
    "black": {
      "level": 20,
      "gallons": 8
    },
    "propane": {
      "level": 60,
      "pounds": 18
    },
    "fuel": {
      "level": 50,
      "gallons": 25,
      "range_miles": 250
    }
  }
}
```

---

## Calibration Guide

### Auto-Calibration Mode

1. Navigate to `/system/settings/tanks`
2. Select tank to calibrate
3. Fill/empty tank to known level
4. Press "Set Calibration Point"
5. Repeat for empty, 25%, 50%, 75%, full

### Manual Resistance Entry

If you know your sensor's resistance values:
```
Tank Configuration:
- Empty resistance: 180Ω
- Full resistance: 10Ω
- Reference resistor: 220Ω
- Sensor type: Linear resistive
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Reading stuck at 0% | Open circuit | Check wiring, sensor connection |
| Reading stuck at 100% | Short circuit | Check for corroded contacts |
| Erratic readings | Poor ground | Ensure chassis ground |
| Readings bounce | Sloshing liquid | Enable averaging filter |

## License

CERN-OHL-S-2.0
