# Vehicle HAT

Leveling, slide-out, and generator control for OpenRoam.

**Estimated Cost:** ~$75 (buy path) / ~$40 (build path)

## Overview

The Vehicle HAT controls motorized vehicle systems including leveling jacks, slide-outs, and generator start/stop. Features auto-level algorithm and position sensing.

## Features

- 4x leveling jack control (30A H-bridge)
- 4x slide-out control
- Generator start/stop
- Position sensing (potentiometers)
- Auto-level algorithm
- Manual override
- Obstruction detection
- Hour meter tracking

## Specifications

### Motor Outputs
| Channel | Type | Rating |
|---------|------|--------|
| Jack 1-4 | H-Bridge | 30A continuous |
| Slide 1-4 | H-Bridge | 30A continuous |
| Generator | Relay | 20A |

### Position Sensing
| Input | Type | Range |
|-------|------|-------|
| Jack 1-4 | Potentiometer | 0-10kΩ |
| Slide 1-4 | Potentiometer | 0-10kΩ |
| Inclinometer | Digital | ±90° |

---

## Option A: Buy Pre-Made Modules

### Components (Buy Path)

| Component | Description | Qty | Price | Source |
|-----------|-------------|-----|-------|--------|
| BTS7960 module | 43A H-bridge | 4 | $5.00 | Amazon/AliExpress |
| STM32G474 Nucleo | Motor control MCU | 1 | $18.00 | DigiKey |
| 10kΩ potentiometer | Position sensor | 8 | $2.00 | DigiKey |
| ICM-42688 breakout | IMU/inclinometer | 1 | $12.00 | SparkFun |
| 30A relay module | Generator control | 1 | $5.00 | Amazon |
| Screw terminals | High current | 12 | $4.00 | DigiKey |
| Carrier PCB | Custom | 1 | $5.00 | JLCPCB |

**Buy Path Total: ~$75**

---

## Option B: Build from Discrete Components

### Components (Build Path)

| Component | Description | Qty | Price | DigiKey PN |
|-----------|-------------|-----|-------|------------|
| BTS7960B | H-bridge IC | 4 | $4.50 | - |
| STM32G474RET6 | MCU | 1 | $6.85 | 497-STM32G474RET6TR-ND |
| ICM-42688-P | IMU | 1 | $4.25 | 1428-ICM-42688-P-ND |
| ADS1115 | ADC | 2 | $4.25 | 296-ADS1115IDGSR-ND |
| IRF3205 | MOSFET | 8 | $0.80 | - |
| IR2110 | Gate driver | 4 | $1.50 | IR2110PBF-ND |
| Current sense | 0.01Ω shunt | 4 | $0.50 | - |
| Passives | R, C, L | 1 set | $5.00 | - |
| PCB | 4-layer | 1 | $8.00 | JLCPCB |

**Build Path Total: ~$40**

### Build from Scratch Options

#### H-Bridge: Build Full Bridge from MOSFETs (Intermediate)

Build a 30A H-bridge motor driver:

**Full H-Bridge Circuit:**
```
         +12V
           │
    ┌──────┴──────┐
    │             │
  Q1(IRF3205)  Q3(IRF3205)
    │             │
    ├──── Motor ──┤
    │             │
  Q2(IRF3205)  Q4(IRF3205)
    │             │
    └──────┬──────┘
           │
          GND

Control Logic:
- Forward:  Q1 ON, Q4 ON, Q2 OFF, Q3 OFF
- Reverse:  Q2 ON, Q3 ON, Q1 OFF, Q4 OFF
- Brake:    Q2 ON, Q4 ON (low-side short)
- Coast:    All OFF
```

**Gate Driver Circuit (IR2110):**
```
              VCC (12V)
                 │
                 │  ┌─────────────────────┐
   PWM_H ────────┼──┤HIN            VB├───┼── Bootstrap
                 │  │                     │   capacitor
                 │  │              HO├───┴── To Q1/Q3 gate
   PWM_L ────────┼──┤LIN               │
                 │  │                     │
   GND ──────────┼──┤VSS           LO├────── To Q2/Q4 gate
                 │  └─────────────────────┘
                 │
             Bootstrap
             diode + cap
```

**Bootstrap Power Supply:**
```
When low-side ON, bootstrap cap charges through diode
When high-side ON, cap provides gate drive voltage
- Use 1µF ceramic + fast diode (1N4148)
- Gate charge: ~50nC for IRF3205
- Minimum ON time: 1µs
```

#### Current Sensing: Build Shunt-Based Sense (Basic)

Build current sensing for motor control:

```
                    Motor+
                       │
                       │
   ┌───────────────────┼───────────────────┐
   │                   │                   │
   │              R_shunt               │
   │              (0.01Ω)               │
   │                   │                   │
   │          ┌────────┴────────┐          │
   │          │                 │          │
   │     ┌────┴────┐       ┌────┴────┐     │
   │     │ SENSE+  │       │ SENSE-  │     │
   │     └────┬────┘       └────┬────┘     │
   │          │                 │          │
   │          └────────┬────────┘          │
   │                   │                   │
   │             Differential           │
   │             Amplifier              │
   │             (INA180)               │
   │                   │                   │
   │                   V_out → ADC         │
   └───────────────────────────────────────┘

V_out = I_motor × R_shunt × Gain
30A × 0.01Ω × 50 = 15V (use 20x gain for 3.3V ADC)
```

**DIY Differential Amplifier:**
```
        R1 (10k)        R2 (100k)
SENSE+ ────┬──── ─┬─────────┬───── VOUT
           │      │   │     │
           │   ┌──┴───┴──┐  │
           │   │ Op-Amp  │  │
           │   │ MCP6002 │  │
           │   └─────────┘  │
           │         │      │
SENSE- ────┴───R3───┴──R4──┘
          (10k)     (100k)

Gain = R2/R1 = 10
Common-mode rejection critical for accuracy
```

#### Auto-Level Algorithm: Implement PID Control (Advanced)

Build auto-leveling system:

**Sensors Required:**
- 2-axis inclinometer (pitch, roll)
- 4x jack position potentiometers
- Ground contact switches (optional)

**Level Algorithm:**
```python
class AutoLevel:
    def __init__(self):
        self.target_pitch = 0.0
        self.target_roll = 0.0
        self.tolerance = 0.5  # degrees

    def calculate_corrections(self, pitch, roll):
        """
        Jack arrangement:
            Front
          LF    RF
            ┌──┐
            │  │
            │  │
            └──┘
          LR    RR
            Rear

        Pitch+ = nose up, Roll+ = right side up
        """
        corrections = {
            'LF': 0, 'RF': 0,
            'LR': 0, 'RR': 0
        }

        # Pitch correction (front/rear)
        if pitch > self.tolerance:
            # Nose high - extend rear jacks
            corrections['LR'] = 1
            corrections['RR'] = 1
        elif pitch < -self.tolerance:
            # Nose low - extend front jacks
            corrections['LF'] = 1
            corrections['RF'] = 1

        # Roll correction (left/right)
        if roll > self.tolerance:
            # Right side high - extend left jacks
            corrections['LF'] = 1
            corrections['LR'] = 1
        elif roll < -self.tolerance:
            # Left side high - extend right jacks
            corrections['RF'] = 1
            corrections['RR'] = 1

        return corrections

    def level_vehicle(self):
        while True:
            pitch, roll = self.read_inclinometer()

            if abs(pitch) < self.tolerance and abs(roll) < self.tolerance:
                print("Vehicle leveled!")
                break

            corrections = self.calculate_corrections(pitch, roll)

            for jack, direction in corrections.items():
                if direction != 0:
                    self.move_jack(jack, direction)

            time.sleep(0.5)  # Movement interval
```

**Safety Limits:**
```python
MAX_EXTENSION = 100  # % of travel
MAX_ANGLE = 15       # degrees from level
TIMEOUT = 120        # seconds

def safe_level(self):
    start_time = time.time()

    while time.time() - start_time < TIMEOUT:
        pitch, roll = self.read_inclinometer()

        # Safety check - excessive angle
        if abs(pitch) > MAX_ANGLE or abs(roll) > MAX_ANGLE:
            self.emergency_stop()
            raise Exception("Excessive tilt detected")

        # Check jack positions
        for jack in self.jacks:
            if jack.position > MAX_EXTENSION:
                self.emergency_stop()
                raise Exception(f"Jack {jack.name} over-extended")

        # Normal leveling logic...
```

---

## Wiring Guide

### Jack Motor Connections

```
Vehicle HAT                    Leveling Jacks
┌─────────────────┐            ┌─────────────────┐
│ JACK1_OUT+ ─────┼────────────┤ Front Left +    │
│ JACK1_OUT- ─────┼────────────┤ Front Left -    │
│                 │            │                 │
│ JACK2_OUT+ ─────┼────────────┤ Front Right +   │
│ JACK2_OUT- ─────┼────────────┤ Front Right -   │
│                 │            │                 │
│ JACK3_OUT+ ─────┼────────────┤ Rear Left +     │
│ JACK3_OUT- ─────┼────────────┤ Rear Left -     │
│                 │            │                 │
│ JACK4_OUT+ ─────┼────────────┤ Rear Right +    │
│ JACK4_OUT- ─────┼────────────┤ Rear Right -    │
│                 │            │                 │
│ +12V_JACK ──────┼────────────┤ Common Power    │
│ GND ────────────┼────────────┤ Common Ground   │
└─────────────────┘            └─────────────────┘
```

### Generator Control

```
Vehicle HAT                    Generator
┌─────────────────┐            ┌─────────────────┐
│ GEN_START ──────┼────────────┤ Start Relay     │
│ GEN_STOP ───────┼────────────┤ Stop Relay      │
│ GEN_RUN ────────┼────────────┤ Run Detect      │
│ GEN_OIL ────────┼────────────┤ Oil Pressure    │
│ GND ────────────┼────────────┤ Common          │
└─────────────────┘            └─────────────────┘
```

---

## Integration

### MQTT Topics

```
openroam/vehicle/leveling/pitch        # degrees
openroam/vehicle/leveling/roll         # degrees
openroam/vehicle/leveling/state        # leveling/level/travel
openroam/vehicle/leveling/command      # auto-level/retract/manual
openroam/vehicle/jack/1/position       # %
openroam/vehicle/jack/1/command        # extend/retract/stop
openroam/vehicle/slide/1/position      # %
openroam/vehicle/slide/1/state         # extending/retracting/stopped
openroam/vehicle/slide/1/command       # extend/retract/stop
openroam/vehicle/generator/state       # running/stopped/cranking
openroam/vehicle/generator/hours       # total run hours
openroam/vehicle/generator/command     # start/stop
```

### RoamK Data

```json
{
  "vehicle": {
    "leveling": {
      "pitch": 0.3,
      "roll": -0.2,
      "state": "level",
      "jacks": {
        "front_left": {"position": 45, "state": "stopped"},
        "front_right": {"position": 48, "state": "stopped"},
        "rear_left": {"position": 52, "state": "stopped"},
        "rear_right": {"position": 50, "state": "stopped"}
      }
    },
    "slides": {
      "main": {"position": 100, "state": "extended"},
      "bedroom": {"position": 100, "state": "extended"}
    },
    "generator": {
      "state": "stopped",
      "hours": 156.7,
      "last_run": "2024-01-15T08:30:00Z"
    }
  }
}
```

---

## Safety Features

### Jack Safety
- Ground contact detection
- Over-current protection
- Position limit switches
- Emergency retract
- Manual bypass

### Slide Safety
- Obstruction detection (current spike)
- Position memory
- Ignition interlock
- Manual override

### Generator Safety
- Low oil shutdown
- Over-crank protection
- Remote fuel shutoff
- Auto-start on low battery

## License

CERN-OHL-S-2.0
