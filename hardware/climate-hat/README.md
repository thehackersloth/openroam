# Climate HAT

Temperature monitoring and HVAC control for OpenRoam.

**Estimated Cost:** ~$45 (buy path) / ~$25 (build path)

## Overview

The Climate HAT provides 8-zone temperature and humidity monitoring with HVAC relay control. Supports diesel heaters (Webasto, Espar, Chinese), rooftop AC, and furnace control.

## Features

- 8 temperature zones
- 4 humidity sensors
- 4x 30A relay outputs for HVAC
- Diesel heater interface (W-Bus, serial)
- Roof AC compressor control
- Furnace ignition control
- Vent fan PWM control
- Temperature scheduling

## Specifications

### Temperature Sensing
| Parameter | Value |
|-----------|-------|
| Zones | 8 |
| Range | -40°C to +125°C |
| Accuracy | ±0.2°C |
| Resolution | 0.01°C |

### Humidity Sensing
| Parameter | Value |
|-----------|-------|
| Channels | 4 |
| Range | 0-100% RH |
| Accuracy | ±2% RH |

### Control Outputs
| Output | Rating |
|--------|--------|
| Relay 1-4 | 30A @ 12V |
| PWM 1-2 | 5A @ 12V |

---

## Option A: Buy Pre-Made Modules

### Components (Buy Path)

| Component | Description | Qty | Price | Source |
|-----------|-------------|-----|-------|--------|
| SHT40 breakout | Temp/humidity | 8 | $4.00 | Adafruit |
| 4-relay module | 30A relays | 1 | $8.00 | Amazon |
| STM32G071 Nucleo | MCU | 1 | $15.00 | DigiKey |
| MOSFET module | PWM output | 2 | $2.00 | Amazon |
| Wiring harness | Sensor cables | 1 | $8.00 | - |
| Carrier PCB | Custom | 1 | $5.00 | JLCPCB |

**Buy Path Total: ~$45**

---

## Option B: Build from Discrete Components

### Components (Build Path)

| Component | Description | Qty | Price | DigiKey PN |
|-----------|-------------|-----|-------|------------|
| SHT40-AD1B-R3 | Temp/humidity IC | 8 | $3.25 | 1649-SHT40-AD1B-R3TR-ND |
| STM32G071RBT6 | MCU | 1 | $4.85 | 497-STM32G071RBT6-ND |
| G5LE-1 | 30A relay | 4 | $2.00 | Z760-ND |
| ULN2003A | Relay driver | 1 | $0.50 | 296-1368-5-ND |
| IRLZ44N | MOSFET | 2 | $0.75 | IRLZ44NPBF-ND |
| 1-Wire header | Sensor bus | 8 | $0.20 | - |
| Passives | R, C | 1 set | $2.00 | - |
| PCB | 2-layer | 1 | $3.00 | JLCPCB |

**Build Path Total: ~$25**

### Build from Scratch Options

#### Temperature Sensor: Build from Thermistor (Basic)

Build precision temperature measurement:

**NTC Thermistor Circuit:**
```
       VCC (3.3V)
          │
          │
       R_ref (10kΩ 0.1%)
          │
          ├───────── To ADC
          │
       NTC (10kΩ @ 25°C)
          │
         GND

Temperature calculation (Steinhart-Hart):
1/T = A + B×ln(R) + C×(ln(R))³

Simplified Beta equation:
T = 1 / (1/T0 + (1/β)×ln(R/R0)) - 273.15

Where:
- T0 = 298.15K (25°C)
- β = 3950 (typical)
- R0 = 10kΩ (resistance at 25°C)
```

**Python Implementation:**
```python
import math

def ntc_to_celsius(adc_value, vcc=3.3, r_ref=10000, beta=3950, r0=10000):
    voltage = adc_value * vcc / 65535  # 16-bit ADC
    r_ntc = r_ref * voltage / (vcc - voltage)

    t_kelvin = 1 / (1/298.15 + (1/beta) * math.log(r_ntc/r0))
    return t_kelvin - 273.15
```

**DIY Precision Reference:**
- Use LM4040 voltage reference for better accuracy
- Or build bandgap reference from transistors

#### Humidity Sensor: Build Capacitive Sensor (Intermediate)

Build a humidity sensor:

**Capacitive Humidity Sensing:**
```
Humidity-sensitive capacitor changes capacitance with moisture:
- Dry: ~150pF
- Wet: ~200pF

Using 555 Timer:
           ┌────────────────────┐
           │                    │
    VCC ───┤8     555     3├─── Frequency out
           │      Timer       │
           │                    │
           ├───────────────────7├─── 100kΩ
           │                    │
           ├───────────────────6├───┬─── Humidity capacitor
           │                    │   │
    GND ───┤1              2├───┘
           └────────────────────┘

f = 1.44 / (R × C)
```

**Polymer Capacitor DIY:**
- Interdigitated PCB electrodes
- Coat with polyimide film
- Film absorbs moisture, changes ε

#### Relay Driver: Build with Discrete Components (Basic)

Build relay driver without ULN2003:

```
                    +12V
                      │
                      │
                   ┌──┴──┐
              Relay│     │Coil
                   └──┬──┘
                      │
             D1 (1N4148)─┤ Flyback protection
                      │
                      C
   GPIO ──── R1 ──── B  Q1 (2N2222)
   (3.3V)   (1kΩ)     E
                      │
                     GND
```

**MOSFET Alternative (better for higher current):**
```
                    +12V
                      │
                   ┌──┴──┐
              Relay│     │Coil
                   └──┬──┘
                      │
             D1 ──────┤
                      │
                      D
   GPIO ──── R1 ──── G  Q1 (IRLZ44N)
             (10kΩ)   S
                      │
                     GND
```

#### Diesel Heater Interface: Build W-Bus Protocol (Advanced)

Build Webasto W-Bus interface:

**W-Bus Physical Layer:**
```
W-Bus is a single-wire protocol:
- Idle: High (5V)
- Bit 0: Low for 52µs, high for 52µs
- Bit 1: Low for 104µs
- Start bit: Low for 104µs
- Byte timing: ~10ms per byte

           5V ─────┐     ┌─────┐     ┌─────────
                   │     │     │     │
           0V      └─────┘     └─────┘

           |--104µs-|--52µs|--104µs--|
              Start    0      1
```

**DIY W-Bus Interface:**
```
                    +5V
                      │
                   R_pullup
                   (4.7kΩ)
                      │
    W-Bus ────────────┼───────── GPIO (input)
                      │
                    Q1 ─────── GPIO (output)
                    (2N7000)
                      │
                     GND
```

**Protocol Implementation:**
```cpp
class WBus {
    int pin;

public:
    WBus(int wbus_pin) : pin(wbus_pin) {
        pinMode(pin, INPUT_PULLUP);
    }

    void sendByte(uint8_t data) {
        // Start bit
        sendBit(1);

        // Data bits (LSB first)
        for (int i = 0; i < 8; i++) {
            sendBit((data >> i) & 1);
        }
    }

    void sendBit(bool bit) {
        pinMode(pin, OUTPUT);
        digitalWrite(pin, LOW);

        if (bit) {
            delayMicroseconds(104);
        } else {
            delayMicroseconds(52);
            digitalWrite(pin, HIGH);
            delayMicroseconds(52);
        }

        pinMode(pin, INPUT_PULLUP);
    }

    void startHeater() {
        // W-Bus command: 0x21 (start heating)
        sendByte(0x21);
    }

    void setTemperature(uint8_t temp_c) {
        // W-Bus command: 0x24 + temperature
        sendByte(0x24);
        sendByte(temp_c);
    }
};
```

---

## Wiring Guide

### Temperature Sensor Placement

```
                    ┌─────────────────────────┐
                    │      Roof AC Unit       │
                    │         Zone 5          │
                    └─────────────────────────┘
                              │
    ┌─────────────────────────┼─────────────────────────┐
    │                         │                         │
    │  Living Area      Bathroom         Bedroom        │
    │    Zone 1          Zone 3          Zone 4         │
    │                                                   │
    │                                                   │
    │     Kitchen/Galley              Cab               │
    │        Zone 2                 Zone 6              │
    │                                                   │
    ├───────────────────────────────────────────────────┤
    │              Basement / Storage                   │
    │                   Zone 7                          │
    └───────────────────────────────────────────────────┘
                              │
                         Zone 8: Exterior
```

### HVAC Control Wiring

```
Climate HAT                      HVAC Equipment
┌─────────────┐                  ┌──────────────┐
│ Relay 1 ────┼──────────────────┤ Roof AC +12V │
│ Relay 2 ────┼──────────────────┤ Furnace Call │
│ Relay 3 ────┼──────────────────┤ Vent Fan Hi  │
│ Relay 4 ────┼──────────────────┤ Vent Fan Lo  │
│             │                  │              │
│ W-Bus ──────┼──────────────────┤ Diesel Htr   │
│             │                  │              │
│ GND ────────┼──────────────────┤ Common       │
└─────────────┘                  └──────────────┘
```

---

## Firmware

### Zone Temperature Control

```cpp
struct ThermostatZone {
    float current_temp;
    float setpoint;
    float hysteresis;
    bool heating;
    bool cooling;
    uint8_t relay;
};

ThermostatZone zones[8];

void controlLoop() {
    for (int i = 0; i < 8; i++) {
        zones[i].current_temp = readTemperature(i);

        // Heating control
        if (zones[i].current_temp < zones[i].setpoint - zones[i].hysteresis) {
            enableHeating(zones[i].relay);
            zones[i].heating = true;
        } else if (zones[i].current_temp > zones[i].setpoint) {
            disableHeating(zones[i].relay);
            zones[i].heating = false;
        }

        // Cooling control (if equipped)
        if (zones[i].current_temp > zones[i].setpoint + zones[i].hysteresis) {
            enableCooling();
            zones[i].cooling = true;
        } else if (zones[i].current_temp < zones[i].setpoint) {
            disableCooling();
            zones[i].cooling = false;
        }
    }
}
```

---

## Integration

### MQTT Topics

```
openroam/climate/zone/1/temperature
openroam/climate/zone/1/humidity
openroam/climate/zone/1/setpoint
openroam/climate/zone/1/mode          # heat/cool/auto/off
openroam/climate/hvac/state           # heating/cooling/idle
openroam/climate/heater/state         # on/off
openroam/climate/heater/command       # on/off/temp
openroam/climate/ac/state
openroam/climate/furnace/state
```

### RoamK Data

```json
{
  "climate": {
    "interior": {
      "temperature": 22.5,
      "humidity": 45
    },
    "exterior": {
      "temperature": 5.0,
      "humidity": 80
    },
    "zones": {
      "living": {"temperature": 22.5, "setpoint": 22.0, "humidity": 45},
      "bedroom": {"temperature": 21.0, "setpoint": 20.0, "humidity": 50},
      "bathroom": {"temperature": 23.0, "setpoint": 22.0, "humidity": 65},
      "cab": {"temperature": 18.0, "setpoint": 18.0, "humidity": 40}
    },
    "hvac": {
      "mode": "heat",
      "running": true,
      "fan_speed": 2
    }
  }
}
```

---

## Diesel Heater Integration

### Supported Heaters

| Brand | Protocol | Interface |
|-------|----------|-----------|
| Webasto | W-Bus | Serial |
| Espar | Proprietary | Serial |
| Chinese (Vevor, etc.) | Simple | Relay or PWM |

### Chinese Diesel Heater Control

Simple relay control for budget heaters:

```cpp
// Basic relay control
void setHeaterLevel(uint8_t level) {
    // Level 0-9 (0 = off)
    analogWrite(HEATER_PWM_PIN, map(level, 0, 9, 0, 255));
}

// Or pulse-based (simulates button press)
void pressHeaterButton(int presses) {
    for (int i = 0; i < presses; i++) {
        digitalWrite(HEATER_BUTTON_PIN, HIGH);
        delay(200);
        digitalWrite(HEATER_BUTTON_PIN, LOW);
        delay(200);
    }
}
```

---

## Safety Features

- Over-temperature shutdown (85°C max)
- CO sensor integration (via Safety HAT)
- Ventilation interlock
- Power failure memory
- Combustion air check

## License

CERN-OHL-S-2.0
