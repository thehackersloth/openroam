# Engine Monitor HAT

OBD-II and J1939 vehicle diagnostics for OpenRoam.

**Estimated Cost:** ~$65 (buy path) / ~$30 (build path)

## Overview

The Engine Monitor HAT provides real-time engine data via OBD-II (gas/light diesel) and J1939 (heavy-duty diesel). Track fuel economy, temperatures, pressures, and diagnostic trouble codes.

## Features

- OBD-II (CAN, ISO 15765)
- J1939 (heavy-duty diesel)
- Real-time data streaming
- DTC reading and clearing
- Fuel consumption tracking
- Temperature/pressure monitoring
- Analog sensor inputs

## Specifications

### OBD-II Support
| Protocol | Description |
|----------|-------------|
| ISO 15765-4 CAN | Most vehicles 2008+ |
| ISO 14230-4 KWP | Korean vehicles |
| ISO 9141-2 | Older European |
| SAE J1850 PWM | Ford |
| SAE J1850 VPW | GM |

### J1939 (Heavy Duty)
| PGN | Description |
|-----|-------------|
| 61444 | Engine RPM, torque |
| 65262 | Engine temp |
| 65263 | Fuel economy |
| 65265 | Vehicle speed |
| 65269 | Exhaust temp |

### Analog Inputs
| Channel | Range | Use |
|---------|-------|-----|
| 1-4 | 0-5V | Temp sensors |
| 5-6 | 4-20mA | Pressure sensors |

---

## Option A: Buy Pre-Made Modules

### Components (Buy Path)

| Component | Description | Qty | Price | Source |
|-----------|-------------|-----|-------|--------|
| ELM327 module | OBD interface | 1 | $15.00 | Amazon |
| MCP2515 module | CAN controller | 1 | $5.00 | Amazon |
| STM32G474 Nucleo | MCU | 1 | $18.00 | DigiKey |
| OBD-II connector | J1962 female | 1 | $8.00 | Amazon |
| ADS1115 module | ADC | 1 | $6.00 | Adafruit |
| Carrier PCB | Custom | 1 | $5.00 | JLCPCB |

**Buy Path Total: ~$65**

---

## Option B: Build from Discrete Components

### Components (Build Path)

| Component | Description | Qty | Price | DigiKey PN |
|-----------|-------------|-----|-------|------------|
| MCP2515 | CAN controller | 1 | $2.50 | MCP2515-I/ST-ND |
| MCP2562 | CAN transceiver | 1 | $1.50 | MCP2562-E/MF-ND |
| STM32G474RET6 | MCU | 1 | $6.85 | 497-STM32G474RET6TR-ND |
| ADS1115 | ADC | 1 | $4.25 | 296-ADS1115IDGSR-ND |
| OBD-II connector | J1962 | 1 | $5.00 | - |
| ESD protection | TVS | 1 | $1.00 | - |
| Passives | R, C, L | 1 set | $3.00 | - |
| PCB | 2-layer | 1 | $3.00 | JLCPCB |

**Build Path Total: ~$30**

### Build from Scratch Options

#### CAN Bus: Build from Discrete Components (Intermediate)

Build CAN transceiver from scratch:

**Discrete CAN Transceiver:**
```
CAN-H ────┬─── R_term (120Ω) ───┬─── CAN-L
          │                     │
          │    ┌────────────┐   │
          ├────┤ Comparator ├───┤
          │    │  (LM393)   │   │
          │    └─────┬──────┘   │
          │          │          │
          │         RX          │
          │                     │
          │    ┌────────────┐   │
          │    │  H-Bridge  │   │
          ├────┤  Driver    ├───┤
          │    │ (2x 2N7000)│   │
          │    └─────┬──────┘   │
          │          │          │
          │         TX          │
          │                     │
         GND                   GND

CAN-H dominant: 3.5V
CAN-L dominant: 1.5V
CAN-H recessive: 2.5V
CAN-L recessive: 2.5V
Differential = 2V (dominant), 0V (recessive)
```

**ISO-TP Implementation (Multi-frame messages):**
```python
class ISOTP:
    """ISO 15765-2 Transport Protocol for multi-frame OBD"""

    def send_message(self, data):
        if len(data) <= 7:
            # Single frame
            frame = bytes([len(data)]) + data
            self.can.send(frame)
        else:
            # Multi-frame
            # First frame
            length = len(data)
            first = bytes([0x10 | (length >> 8), length & 0xFF]) + data[:6]
            self.can.send(first)

            # Wait for flow control
            fc = self.can.receive(timeout=1000)
            block_size = fc[1]
            sep_time = fc[2]

            # Consecutive frames
            seq = 1
            offset = 6
            while offset < len(data):
                chunk = data[offset:offset+7]
                frame = bytes([0x20 | (seq & 0x0F)]) + chunk
                self.can.send(frame)
                seq += 1
                offset += 7
                time.sleep(sep_time / 1000)

    def receive_message(self):
        frame = self.can.receive()
        pci = frame[0]

        if pci <= 0x07:
            # Single frame
            return frame[1:1+pci]

        elif (pci & 0xF0) == 0x10:
            # First frame
            length = ((pci & 0x0F) << 8) | frame[1]
            data = bytearray(frame[2:])

            # Send flow control
            self.can.send(bytes([0x30, 0x00, 0x00]))

            # Receive consecutive frames
            while len(data) < length:
                cf = self.can.receive()
                data.extend(cf[1:])

            return bytes(data[:length])
```

#### OBD-II PID Decoder: Implement All PIDs (Intermediate)

Build complete OBD-II decoder:

```python
class OBD2:
    PIDS = {
        0x00: ('PIDS_SUPPORTED', lambda d: d),
        0x04: ('ENGINE_LOAD', lambda d: d[0] * 100 / 255),
        0x05: ('COOLANT_TEMP', lambda d: d[0] - 40),
        0x06: ('SHORT_FUEL_TRIM_1', lambda d: (d[0] - 128) * 100 / 128),
        0x07: ('LONG_FUEL_TRIM_1', lambda d: (d[0] - 128) * 100 / 128),
        0x0B: ('INTAKE_PRESSURE', lambda d: d[0]),  # kPa
        0x0C: ('RPM', lambda d: (d[0] * 256 + d[1]) / 4),
        0x0D: ('SPEED', lambda d: d[0]),  # km/h
        0x0E: ('TIMING_ADVANCE', lambda d: d[0] / 2 - 64),
        0x0F: ('INTAKE_TEMP', lambda d: d[0] - 40),
        0x10: ('MAF_RATE', lambda d: (d[0] * 256 + d[1]) / 100),  # g/s
        0x11: ('THROTTLE', lambda d: d[0] * 100 / 255),
        0x1F: ('RUN_TIME', lambda d: d[0] * 256 + d[1]),  # seconds
        0x2F: ('FUEL_LEVEL', lambda d: d[0] * 100 / 255),
        0x5C: ('OIL_TEMP', lambda d: d[0] - 40),
        0x5E: ('FUEL_RATE', lambda d: (d[0] * 256 + d[1]) / 20),  # L/h
    }

    def __init__(self, can):
        self.can = can

    def request_pid(self, pid):
        # Send request (CAN ID 0x7DF = broadcast)
        request = bytes([0x02, 0x01, pid, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.can.send(0x7DF, request)

        # Receive response (CAN ID 0x7E8-0x7EF)
        response = self.can.receive(timeout=100)
        if response and response[1] == 0x41:
            return response[3:]
        return None

    def read_pid(self, pid):
        data = self.request_pid(pid)
        if data and pid in self.PIDS:
            name, decoder = self.PIDS[pid]
            return name, decoder(data)
        return None, None

    def read_dtcs(self):
        """Read Diagnostic Trouble Codes"""
        request = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.can.send(0x7DF, request)
        response = self.can.receive()

        dtcs = []
        if response and response[1] == 0x43:
            num_codes = response[2]
            for i in range(num_codes):
                byte1 = response[3 + i*2]
                byte2 = response[4 + i*2]
                dtcs.append(self.decode_dtc(byte1, byte2))
        return dtcs

    def decode_dtc(self, b1, b2):
        prefix = ['P', 'C', 'B', 'U'][(b1 >> 6) & 0x03]
        digit1 = (b1 >> 4) & 0x03
        digit2 = b1 & 0x0F
        digit3 = (b2 >> 4) & 0x0F
        digit4 = b2 & 0x0F
        return f"{prefix}{digit1}{digit2:X}{digit3:X}{digit4:X}"
```

#### J1939 Protocol: Heavy-Duty Diesel (Advanced)

Build J1939 decoder for commercial vehicles:

```python
class J1939:
    """SAE J1939 Protocol for heavy-duty vehicles"""

    # Parameter Group Numbers (PGNs)
    PGNS = {
        61444: 'EEC1',  # Electronic Engine Controller 1
        65262: 'ET1',   # Engine Temperature 1
        65263: 'EFL/P', # Fuel Economy
        65265: 'CCVS',  # Cruise Control/Vehicle Speed
        65269: 'AMB',   # Ambient Conditions
        65270: 'IC1',   # Inlet/Exhaust Conditions
    }

    def parse_eec1(self, data):
        """Parse Engine Controller message"""
        return {
            'engine_torque_mode': data[0] & 0x0F,
            'driver_demand_torque': data[1] - 125,  # %
            'actual_torque': data[2] - 125,  # %
            'rpm': (data[4] << 8 | data[3]) * 0.125,
            'source_address': data[5],
        }

    def parse_et1(self, data):
        """Parse Engine Temperature message"""
        return {
            'coolant_temp': data[0] - 40,  # °C
            'fuel_temp': data[1] - 40,  # °C
            'oil_temp': (data[3] << 8 | data[2]) * 0.03125 - 273,  # °C
        }

    def parse_fuel_economy(self, data):
        """Parse Fuel Economy message"""
        return {
            'fuel_rate': (data[1] << 8 | data[0]) * 0.05,  # L/h
            'instant_fuel_economy': (data[3] << 8 | data[2]) / 512,  # km/L
            'avg_fuel_economy': (data[5] << 8 | data[4]) / 512,  # km/L
        }

    def receive_message(self):
        """Receive and parse J1939 message"""
        can_id, data = self.can.receive()

        # Extract PGN from 29-bit CAN ID
        pgn = (can_id >> 8) & 0x3FFFF
        source = can_id & 0xFF

        if pgn in self.PGNS:
            parser = getattr(self, f'parse_{self.PGNS[pgn].lower()}', None)
            if parser:
                return self.PGNS[pgn], parser(data)

        return pgn, data
```

---

## Firmware

### Real-Time Data Streaming

```cpp
#include <mcp_can.h>

MCP_CAN can(10);  // CS pin

struct EngineData {
    uint16_t rpm;
    uint8_t coolant_temp;
    uint8_t oil_temp;
    uint8_t throttle;
    uint16_t speed;
    float fuel_rate;
    float mpg_instant;
} engine;

void readOBD() {
    static const uint8_t pids[] = {0x0C, 0x05, 0x5C, 0x11, 0x0D, 0x5E};

    for (uint8_t pid : pids) {
        uint8_t request[8] = {0x02, 0x01, pid, 0x55, 0x55, 0x55, 0x55, 0x55};
        can.sendMsgBuf(0x7DF, 0, 8, request);

        unsigned long timeout = millis() + 100;
        while (millis() < timeout) {
            if (can.checkReceive() == CAN_MSGAVAIL) {
                uint8_t len;
                uint8_t buf[8];
                can.readMsgBuf(&len, buf);

                if (buf[1] == 0x41 && buf[2] == pid) {
                    parsePID(pid, &buf[3]);
                    break;
                }
            }
        }
    }
}

void parsePID(uint8_t pid, uint8_t* data) {
    switch (pid) {
        case 0x0C: engine.rpm = ((data[0] << 8) | data[1]) / 4; break;
        case 0x05: engine.coolant_temp = data[0] - 40; break;
        case 0x5C: engine.oil_temp = data[0] - 40; break;
        case 0x11: engine.throttle = data[0] * 100 / 255; break;
        case 0x0D: engine.speed = data[0]; break;
        case 0x5E: engine.fuel_rate = ((data[0] << 8) | data[1]) / 20.0; break;
    }
}
```

---

## Integration

### MQTT Topics

```
openroam/engine/rpm
openroam/engine/coolant_temp
openroam/engine/oil_temp
openroam/engine/oil_pressure
openroam/engine/throttle
openroam/engine/load
openroam/engine/speed
openroam/engine/fuel_rate
openroam/engine/mpg_instant
openroam/engine/mpg_average
openroam/engine/dtc_codes
openroam/engine/check_engine
```

### RoamK Data

```json
{
  "engine": {
    "rpm": 2100,
    "coolant_temp": 195,
    "oil_temp": 210,
    "oil_pressure": 45,
    "trans_temp": 175,
    "throttle": 25,
    "load": 35,
    "fuel_rate": 2.5,
    "mpg_instant": 12.5,
    "mpg_average": 10.2,
    "dtc_codes": [],
    "check_engine": false
  }
}
```

## License

CERN-OHL-S-2.0
