# LoRa Mesh HAT

Off-grid messaging and convoy tracking for OpenRoam.

**Estimated Cost:** ~$55 (buy path) / ~$25 (build path)

## Overview

The LoRa Mesh HAT provides long-range, low-power radio communication for off-grid messaging, convoy tracking, and emergency beacons. Compatible with Meshtastic firmware for interoperability with other devices.

## Features

- LoRa transceiver (SX1262)
- 915 MHz ISM band (US)
- 10+ mile range (line of sight)
- Mesh networking (store and forward)
- Meshtastic compatible
- GPS position sharing
- Text messaging
- Emergency beacon
- Solar/battery powered option

## Specifications

### Radio
| Parameter | Value |
|-----------|-------|
| Frequency | 902-928 MHz (US) |
| TX Power | 22 dBm (+30 dBm with PA) |
| RX Sensitivity | -137 dBm |
| Modulation | LoRa CSS |
| Data Rate | 300 bps - 37.5 kbps |

### Range
| Environment | Typical Range |
|-------------|---------------|
| Line of sight | 10-15 miles |
| Suburban | 2-5 miles |
| Forest/hills | 1-3 miles |
| Urban | 0.5-2 miles |

---

## Option A: Buy Pre-Made Modules

### Components (Buy Path)

| Component | Description | Qty | Price | Source |
|-----------|-------------|-----|-------|--------|
| LILYGO T-Beam | ESP32 + LoRa + GPS | 1 | $35.00 | AliExpress |
| SMA antenna | 915MHz | 1 | $5.00 | Amazon |
| Pi HAT adapter | GPIO breakout | 1 | $8.00 | Custom |
| Enclosure | 3D printed | 1 | $5.00 | Print |

**Buy Path Total: ~$55**

Or build HAT with module:

| Component | Description | Qty | Price | Source |
|-----------|-------------|-----|-------|--------|
| E22-900M30S | SX1262 module | 1 | $15.00 | Ebyte |
| ESP32-S3-WROOM | MCU | 1 | $4.00 | DigiKey |
| SMA connector | Antenna | 1 | $2.00 | DigiKey |
| Pi HAT PCB | Custom | 1 | $5.00 | JLCPCB |
| Passives | R, C | 1 set | $3.00 | - |

---

## Option B: Build from Discrete Components

### Components (Build Path)

| Component | Description | Qty | Price | DigiKey PN |
|-----------|-------------|-----|-------|------------|
| SX1262 | LoRa transceiver | 1 | $5.00 | 1465-SX1262IMLTRT-ND |
| ESP32-S3-WROOM | MCU module | 1 | $3.50 | 1965-ESP32-S3-WROOM-1-N4-ND |
| TCXO 32MHz | Reference | 1 | $2.00 | - |
| RF switch | TX/RX | 1 | $1.50 | - |
| RF matching | L, C | 1 set | $1.00 | - |
| SMA connector | Antenna | 1 | $1.50 | CONSMA001-ND |
| Passives | R, C | 1 set | $2.00 | - |
| PCB | 4-layer RF | 1 | $5.00 | JLCPCB |

**Build Path Total: ~$25**

### Build from Scratch Options

#### LoRa Radio: Build Complete RF Chain (Expert)

Build a LoRa transceiver from fundamental components:

**RF Front-End Architecture:**
```
                    ┌─────────────────────────────────────┐
                    │                                     │
Antenna ────┬───────┤ RF Switch (SKY13317)                │
            │       │     │                               │
            │       │     ├── TX Path                     │
            │       │     │    │                          │
            │       │     │    PA (SKY66112)              │
            │       │     │    │                          │
            │       │     │    Matching Network           │
            │       │     │    │                          │
            │       │     │    └── SX1262 TX              │
            │       │     │                               │
            │       │     └── RX Path                     │
            │       │          │                          │
            │       │          LNA (SKY67150)             │
            │       │          │                          │
            │       │          SAW Filter (915MHz)        │
            │       │          │                          │
            │       │          └── SX1262 RX              │
            │       │                                     │
            │       └─────────────────────────────────────┘
            │
           ESD (TVS diode)
```

**DIY Power Amplifier (PA):**
```
For +30dBm output:
- Use SKY66112 or RFX2411N
- Or build Class-E PA:
  - Driver transistor (2N3904)
  - Final transistor (MRF101AN)
  - Matching network (calculated for 50Ω)
  - Harmonic filter (low-pass)

Class-E PA advantages:
- High efficiency (80%+)
- Simple topology
- Suitable for constant-envelope modulation
```

**Matching Network Calculator:**
```python
import math

def lc_match(z_source, z_load, freq_hz):
    """
    L-network matching calculator
    Returns L and C values for 50Ω match
    """
    omega = 2 * math.pi * freq_hz
    q_factor = math.sqrt(z_source / z_load - 1)

    # High-pass L-network
    l_series = z_source / (omega * q_factor)
    c_shunt = 1 / (omega * z_load * q_factor)

    return l_series, c_shunt

# Example: 915MHz match
l, c = lc_match(50, 10, 915e6)
print(f"L = {l*1e9:.2f} nH")
print(f"C = {c*1e12:.2f} pF")
```

#### Antenna: Build Your Own 915MHz Antenna (Basic)

**Quarter-Wave Ground Plane:**
```
           ┌─── Radiator (81mm vertical)
           │
           │
    ───────┼─────── Ground radials (4x 86mm @ 45°)
           │
         ──┴──
         Coax center to radiator
         Coax shield to radials
```

**Calculation:**
```
λ = c / f = 299792458 / 915000000 = 328mm
λ/4 = 82mm (radiator length)
Radials slightly longer for 45° droop
```

**Yagi-Uda Antenna (Directional):**
```
     Reflector    Driven      Director 1   Director 2
        │           │            │            │
        │           │            │            │
        │           │            │            │
        │           │            │            │
        │           │            │            │
    ────┴───────────┴────────────┴────────────┴────
         170mm       164mm         156mm       148mm

Element spacing: 80mm
Gain: ~9 dBi
```

**Collinear Array (High Gain Omni):**
```
           │ λ/2 element (164mm)
           │
          ───
           │ Phasing stub
          ───
           │ λ/2 element (164mm)
           │
          ───
           │ Phasing stub
          ───
           │ λ/2 element (164mm)
           │

Each element adds ~3 dB gain
4-element = ~10 dBi gain
```

**PCB Antenna (Compact):**
```
Design meandered PCB trace antenna:
- FR4 substrate (εr = 4.4)
- Wavelength shortened by √εr
- λ/4 on PCB ≈ 39mm
- Meander for size reduction

Use free tools:
- 4NEC2 for simulation
- OpenEMS for PCB antennas
```

#### Mesh Protocol: Implement Custom Mesh Network (Advanced)

Build mesh networking from scratch:

**Simple Flooding Protocol:**
```python
import time
import hashlib

class MeshNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.seen_messages = set()
        self.neighbors = []
        self.message_queue = []

    def create_message(self, payload):
        msg = {
            'id': hashlib.sha256(f"{time.time()}{self.node_id}".encode()).hexdigest()[:8],
            'origin': self.node_id,
            'ttl': 5,  # Max hops
            'timestamp': time.time(),
            'payload': payload
        }
        return msg

    def receive_message(self, msg):
        # Dedup
        if msg['id'] in self.seen_messages:
            return None
        self.seen_messages.add(msg['id'])

        # Process locally
        self.handle_message(msg)

        # Rebroadcast if TTL > 0
        if msg['ttl'] > 0:
            msg['ttl'] -= 1
            self.broadcast(msg)

        return msg

    def broadcast(self, msg):
        # Random delay to prevent collisions
        delay = random.uniform(0.1, 0.5)
        time.sleep(delay)
        self.radio.transmit(msg)
```

**More Efficient: AODV-like Routing:**
```python
class AODVMesh(MeshNode):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.routing_table = {}  # dest -> next_hop

    def send_unicast(self, dest, payload):
        if dest in self.routing_table:
            # Known route
            next_hop = self.routing_table[dest]
            self.radio.send_to(next_hop, payload)
        else:
            # Route discovery
            self.send_route_request(dest)
            self.message_queue.append((dest, payload))

    def send_route_request(self, dest):
        rreq = {
            'type': 'RREQ',
            'origin': self.node_id,
            'dest': dest,
            'seq': self.get_seq(),
            'hop_count': 0
        }
        self.broadcast(rreq)

    def handle_route_reply(self, rrep):
        # Update routing table
        self.routing_table[rrep['dest']] = rrep['last_hop']

        # Send queued messages
        for dest, payload in self.message_queue:
            if dest == rrep['dest']:
                self.send_unicast(dest, payload)
```

---

## Firmware

### Meshtastic Configuration

```cpp
// platformio.ini
[env:rak4631]
platform = nordicnrf52
board = wiscore_rak4631
framework = arduino
lib_deps =
    meshtastic/Meshtastic-device

// Custom pins for Pi HAT
build_flags =
    -DPIO_SPI_MISO=19
    -DPIO_SPI_MOSI=23
    -DPIO_SPI_SCK=18
    -DLORA_CS=8
    -DLORA_DIO1=22
    -DLORA_RESET=25
```

### Custom Convoy Tracking

```cpp
// Convoy message format
struct ConvoyPosition {
    uint8_t vehicle_id;
    int32_t latitude;   // degrees * 1e7
    int32_t longitude;
    uint16_t speed;     // knots * 100
    uint16_t heading;   // degrees * 100
    uint8_t status;     // 0=OK, 1=STOPPED, 2=EMERGENCY
};

void broadcastPosition() {
    ConvoyPosition pos;
    pos.vehicle_id = MY_ID;
    pos.latitude = gps.getLatitude();
    pos.longitude = gps.getLongitude();
    pos.speed = gps.getSpeed() * 100;
    pos.heading = gps.getHeading() * 100;
    pos.status = getVehicleStatus();

    mesh.sendBroadcast((uint8_t*)&pos, sizeof(pos));
}
```

---

## Integration

### MQTT Topics

```
openroam/radio/lora/status           # connected/disconnected
openroam/radio/lora/messages/rx      # Received messages
openroam/radio/lora/messages/tx      # Outgoing messages
openroam/radio/lora/convoy/vehicles  # JSON array of convoy positions
openroam/radio/lora/nodes            # Mesh network nodes
openroam/radio/lora/signal           # Last message RSSI/SNR
```

### RoamK Data

```json
{
  "radio": {
    "lora": {
      "status": "connected",
      "nodes": 5,
      "rssi": -85,
      "snr": 9.5,
      "convoy": [
        {
          "id": "Alpha",
          "lat": 35.123,
          "lon": -106.456,
          "speed": 55,
          "heading": 270,
          "distance_mi": 0.5,
          "status": "ok"
        },
        {
          "id": "Bravo",
          "lat": 35.120,
          "lon": -106.460,
          "speed": 53,
          "heading": 270,
          "distance_mi": 1.2,
          "status": "ok"
        }
      ]
    }
  }
}
```

---

## Use Cases

### Convoy Tracking
- Real-time position of all vehicles
- Speed and heading display
- Lost vehicle alerts
- Group messaging

### Off-Grid Messaging
- Text messages without cell service
- Emergency SOS beacon
- Weather updates
- Campground coordination

### Integration with Other Radios
- Bridge to CB/GMRS
- APRS gateway
- Winlink gateway

## License

CERN-OHL-S-2.0
