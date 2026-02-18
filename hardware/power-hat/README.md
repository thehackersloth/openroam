# Power HAT

Battery, solar, and shore power monitoring for OpenRoam.

**Estimated Cost:** ~$65 (buy path) / ~$35 (build path)

## Overview

The Power HAT monitors up to 4 battery banks, solar input, shore power, and alternator charging. It integrates with Victron VE.Direct devices and provides high-accuracy coulomb counting for state of charge.

## Features

- 4x battery bank monitoring (voltage, current, SOC)
- Solar input tracking (watts, daily yield)
- Shore power detection
- Alternator charging detection
- Victron VE.Direct interface (up to 4 devices)
- Victron VE.Can / RV-C (CAN bus)
- Renogy RS-485 interface
- Temperature compensation
- 2500V isolation on power inputs

## Specifications

### Input Ranges
| Parameter | Value |
|-----------|-------|
| Battery Voltage | 10-60V DC (12V, 24V, 48V systems) |
| Current Range | ±200A per channel (Hall effect) |
| Voltage Accuracy | 0.1% |
| Current Accuracy | 0.5% |

### Communication
| Interface | Description |
|-----------|-------------|
| VE.Direct | 3.3V UART, JST connector |
| VE.Can | CAN 2.0B, 250kbps |
| RS-485 | Renogy protocol |
| I2C | Sensor expansion |

---

## Option A: Buy Pre-Made Modules

### Components (Buy Path)

| Component | Description | Qty | Price | Source |
|-----------|-------------|-----|-------|--------|
| INA228 breakout | Power monitor | 4 | $8.00 | Adafruit or custom |
| ADS1115 breakout | 16-bit ADC | 2 | $6.00 | Adafruit 1085 |
| ISO1541 breakout | I2C isolator | 2 | $8.00 | Custom |
| STM32G071 Nucleo | MCU dev board | 1 | $15.00 | DigiKey |
| Shunt resistors | 100A/75mV | 4 | $5.00 | eBay/Amazon |
| VE.Direct cable | Victron | 1 | $12.00 | Victron dealer |
| Screw terminals | 5mm 30A | 8 | $3.00 | DigiKey |
| Carrier PCB | Custom | 1 | $5.00 | JLCPCB |

**Buy Path Total: ~$65**

---

## Option B: Build from Discrete Components

### Components (Build Path)

| Component | Description | Qty | Price | DigiKey PN |
|-----------|-------------|-----|-------|------------|
| INA228AIDGSR | Power monitor IC | 4 | $6.50 | 296-INA228AIDGSR-ND |
| ADS1115IDGSR | 16-bit ADC | 2 | $4.25 | 296-ADS1115IDGSR-ND |
| ISO1541DR | I2C isolator | 2 | $2.85 | 296-ISO1541DR-ND |
| STM32G071RBT6 | MCU | 1 | $4.85 | 497-STM32G071RBT6-ND |
| Shunt resistor | 100µΩ 1% | 4 | $2.00 | WSL2512R1000FEA-ND |
| TVS diodes | SMBJ60A | 8 | $0.30 | SMBJ60A-TPMSCT-ND |
| Screw terminals | 5mm pitch | 8 | $0.45 | ED2609-ND |
| Passives | R, C, L | 1 set | $3.00 | - |
| PCB | 2-layer | 1 | $3.00 | JLCPCB |

**Build Path Total: ~$35**

### Build from Scratch Options

#### Current Sensing: Build Your Own Hall Effect Sensor (Intermediate)

Build a current sensor using Hall effect principle:

**Option 1: Open-Loop Hall Sensor**
```
Components:
- Hall effect IC (ACS712, ACS758, or SS49E)
- Ferrite core (toroidal)
- Op-amp for signal conditioning
- Reference voltage for zero-current

Theory:
1. Current through conductor creates magnetic field
2. Hall element detects field strength
3. Output voltage proportional to current
4. Bandwidth ~80kHz, accuracy ~1%
```

**Option 2: Closed-Loop (Flux-Null) Sensor**
```
Components:
- Hall effect IC
- Compensation winding
- Op-amp feedback loop
- Precision shunt for feedback

Advantages:
- Higher accuracy (~0.1%)
- Better linearity
- Lower temperature drift
- Higher bandwidth
```

**Option 3: DIY Rogowski Coil (AC only)**
```
Components:
- Air-core coil (wind your own)
- Integrator circuit
- No core saturation!

For AC current measurement only (inverter output)
```

#### Voltage Sensing: Build Precision Voltage Divider (Basic)

Build isolated voltage sensing:

**High-Voltage Divider:**
```
               ┌─── R1 (100k 0.1%) ───┐
    V_BATT ───┤                       ├─── To ADC
              │  R2 (4.7k 0.1%)       │
              └───────┬───────────────┘
                      │
                     GND

Ratio: Vin / (R1+R2) * R2 = Vin / 22.27
60V max → 2.69V output (safe for 3.3V ADC)
```

**Isolated Sensing (for shore power):**
```
Components:
- ACPL-C87A isolated amplifier
- Or AMC1311 isolated amp
- Or optocoupler + precision reference

Build from discrete:
- Linear optocoupler (IL300)
- Matched photodiode feedback
- Precision op-amps
```

#### State of Charge: Implement Coulomb Counting (Software)

Build SOC estimation algorithm:

```python
class BatterySOC:
    def __init__(self, capacity_ah):
        self.capacity = capacity_ah
        self.soc = 100.0
        self.last_voltage = 0

    def update(self, current_a, voltage_v, dt_sec):
        # Coulomb counting
        ah_delta = current_a * (dt_sec / 3600)
        self.soc -= (ah_delta / self.capacity) * 100

        # Voltage correction at rest
        if abs(current_a) < 0.5:  # Resting
            self.soc = self.voltage_to_soc(voltage_v)

        # Clamp
        self.soc = max(0, min(100, self.soc))

    def voltage_to_soc(self, v):
        # LiFePO4 lookup table
        # Customize for your battery chemistry
        table = [
            (13.6, 100), (13.4, 90), (13.3, 80),
            (13.2, 70), (13.1, 50), (13.0, 30),
            (12.8, 20), (12.0, 10), (10.0, 0)
        ]
        # Interpolate...
```

---

## Schematic

### Power Input Stage

```
                          ┌────────────────────┐
    BATT+ ────┬───────────┤ TVS Diode SMBJ60A  │
              │           └────────────────────┘
              │                    │
              │    ┌───────────────┴───────────────┐
              │    │                               │
              ├────┤ R_SHUNT (100µΩ)               │
              │    │                               │
              │    └───────┬───────────────────────┘
              │            │
              │    ┌───────┴───────┐
              │    │    INA228     │
              │    │  (I2C addr)   │
              │    └───────────────┘
              │
    BATT- ────┴── GND (isolated)
```

### Victron VE.Direct Interface

```
                    ┌─────────────┐
    VE.Direct TX ───┤ Level shift ├─── UART RX (3.3V)
                    │  (voltage   │
    VE.Direct RX ───┤   divider)  ├─── UART TX (3.3V)
                    └─────────────┘

    VE.Direct is 5V logic, needs 5V→3.3V on RX
    3.3V TX is compatible with 5V input
```

---

## Firmware

### VE.Direct Parser

```cpp
// Victron VE.Direct text protocol parser
class VEDirect {
public:
    struct Data {
        float voltage;      // V
        float current;      // A
        float power;        // W
        float soc;          // %
        int state;          // Charger state
    };

    bool parse(const char* line, Data& data) {
        char label[16], value[32];
        if (sscanf(line, "%15[^\t]\t%31s", label, value) != 2)
            return false;

        if (strcmp(label, "V") == 0)
            data.voltage = atof(value) / 1000.0;
        else if (strcmp(label, "I") == 0)
            data.current = atof(value) / 1000.0;
        else if (strcmp(label, "P") == 0)
            data.power = atof(value);
        else if (strcmp(label, "SOC") == 0)
            data.soc = atof(value) / 10.0;
        // ... more fields

        return true;
    }
};
```

### INA228 Driver

```cpp
#include <Wire.h>

class INA228 {
    uint8_t addr;
    float shunt_ohms;
    float current_lsb;

public:
    INA228(uint8_t address, float shunt)
        : addr(address), shunt_ohms(shunt) {
        // Set current LSB for ±200A range
        current_lsb = 200.0 / 524288.0;
    }

    void begin() {
        Wire.begin();
        // Configure for continuous measurement
        writeReg(0x00, 0x4F27); // CONFIG
        writeReg(0x02, calculateShuntCal()); // SHUNT_CAL
    }

    float readVoltage() {
        uint32_t raw = readReg24(0x05);
        return raw * 195.3125e-6; // 195.3125µV/LSB
    }

    float readCurrent() {
        int32_t raw = (int32_t)readReg24(0x07);
        if (raw & 0x800000) raw |= 0xFF000000; // Sign extend
        return raw * current_lsb;
    }

    float readPower() {
        uint32_t raw = readReg24(0x08);
        return raw * 3.2 * current_lsb;
    }

private:
    void writeReg(uint8_t reg, uint16_t val) {
        Wire.beginTransmission(addr);
        Wire.write(reg);
        Wire.write(val >> 8);
        Wire.write(val & 0xFF);
        Wire.endTransmission();
    }

    uint32_t readReg24(uint8_t reg) {
        Wire.beginTransmission(addr);
        Wire.write(reg);
        Wire.endTransmission();
        Wire.requestFrom(addr, (uint8_t)3);
        uint32_t val = Wire.read() << 16;
        val |= Wire.read() << 8;
        val |= Wire.read();
        return val;
    }

    uint16_t calculateShuntCal() {
        return (uint16_t)(13107.2e6 * current_lsb * shunt_ohms);
    }
};
```

---

## Integration

### MQTT Topics

```
openroam/power/battery/house/voltage     # V
openroam/power/battery/house/current     # A (+ charging, - discharging)
openroam/power/battery/house/soc         # %
openroam/power/battery/house/temp        # °C
openroam/power/battery/chassis/voltage
openroam/power/solar/voltage
openroam/power/solar/current
openroam/power/solar/watts
openroam/power/solar/daily_wh
openroam/power/shore/connected           # true/false
openroam/power/shore/voltage
openroam/power/shore/current
openroam/power/alternator/charging
openroam/power/alternator/current
```

### RoamK Data

```json
{
  "power": {
    "batteries": {
      "house": {
        "voltage": 13.2,
        "current": -5.5,
        "soc": 85,
        "temp": 25,
        "capacity_ah": 200
      },
      "chassis": {
        "voltage": 12.8,
        "current": 0,
        "soc": 100
      }
    },
    "solar": {
      "voltage": 35.2,
      "current": 12.8,
      "watts": 450,
      "daily_wh": 2800,
      "lifetime_kwh": 1250
    },
    "shore": {
      "connected": false,
      "voltage": 0,
      "amps": 0
    },
    "alternator": {
      "charging": true,
      "amps": 45
    }
  }
}
```

---

## Wiring Guide

### Battery Connections

```
House Bank (+) ───┬─── Shunt (+) ──── Shunt (S+) ──── HAT BATT1+
                  │
                  └─── Fuse 200A ──── To loads

House Bank (-) ───────────────────── Shunt (-) ──── HAT BATT1-
                                     (System ground)
```

### Victron Connection

```
Victron MPPT/BMV                Power HAT
  VE.Direct                     VE.Direct
  ┌────────┐                    ┌────────┐
  │ +5V    │────────────────────│ +5V    │
  │ TX     │────────────────────│ RX     │
  │ RX     │────────────────────│ TX     │
  │ GND    │────────────────────│ GND    │
  └────────┘                    └────────┘
```

---

## Safety Notes

- Always fuse battery connections
- Use appropriately rated wire (4 AWG for 200A)
- Install shunts on negative lead
- Ensure proper isolation for high voltages
- Shore power sensing requires proper isolation

## License

CERN-OHL-S-2.0
