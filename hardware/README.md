# OpenRoam Hardware

Open-source hardware modules for mobile living vehicle monitoring and control.

## Design Philosophy: Buy or Build

OpenRoam embraces the full maker spectrum. Every module offers two paths:

### Buy Option (Quick Start)
Use pre-made modules and breakout boards for fast assembly:
- Tested, proven components
- Minimal soldering required
- Get up and running quickly

### Build Option (Full DIY)
Build from discrete components for complete understanding and customization:
- Full schematics provided
- Theory of operation documented
- Maximum flexibility and learning

**You choose your adventure.** Mix and match - buy a GPS module but build your own power monitoring circuit.

## Module Categories

### Core Cluster HATs
Essential modules for the 4-node cluster:

| Module | Cost | Description |
|--------|------|-------------|
| [Nav HAT](nav-hat/) | ~$85 | GPS, IMU, compass, sensor hub |
| [Power HAT](power-hat/) | ~$65 | Battery/solar/shore monitoring |
| [Storage HAT](storage-hat/) | ~$55 | NVMe storage for NAS node |
| [AI Carrier](ai-carrier/) | ~$65 | Hailo-8L AI accelerator |

### RV-Specific HATs
Vehicle system monitoring and control:

| Module | Cost | Description |
|--------|------|-------------|
| [Tank HAT](tank-hat/) | ~$55 | Water/fuel/propane levels |
| [Climate HAT](climate-hat/) | ~$45 | Temperature zones, HVAC control |
| [Vehicle HAT](vehicle-hat/) | ~$75 | Leveling, slides, generator |
| [Safety HAT](safety-hat/) | ~$35 | Smoke/CO/propane detection |

### Network & Communications
Connectivity modules:

| Module | Cost | Description |
|--------|------|-------------|
| [Router HAT](router-hat/) | ~$75 | WiFi 6 AP, mesh networking |
| [Cellular Interface](cellular-interface/) | ~$85 | LTE/5G modem |
| [LoRa Mesh HAT](lora-mesh-hat/) | ~$55 | Off-grid messaging |

### Radio Communications
RF interfaces:

| Module | Cost | Description |
|--------|------|-------------|
| [CB Radio Interface](cb-radio-interface/) | ~$45 | CB control |
| [GMRS Interface](gmrs-interface/) | ~$35 | GMRS/FRS radio |
| [Ham Radio Interface](ham-radio-interface/) | ~$65 | HF/VHF/UHF rig control |
| [SDR Receiver](sdr-receiver/) | ~$45 | Wideband SDR |
| [AM/FM Tuner HAT](amfm-tuner-hat/) | ~$35 | Broadcast radio |

### Interface Modules
Peripheral connections:

| Module | Cost | Description |
|--------|------|-------------|
| [Lighting HAT](lighting-hat/) | ~$45 | LED dimming, scenes |
| [Camera Interface](camera-interface/) | ~$65 | 4x MIPI CSI |
| [Audio Interface](audio-interface/) | ~$45 | Bluetooth, zones |
| [Engine Monitor HAT](engine-monitor-hat/) | ~$65 | OBD-II, J1939 |
| [Dash Display Interface](dash-display-interface/) | ~$45 | 7" touchscreen |
| [Gaming HAT](gaming-hat/) | ~$55 | Controllers, retro gaming |
| [Media Controller](media-controller/) | ~$35 | IR learning, knobs |
| [Inverter Interface](inverter-interface/) | ~$35 | Inverter monitoring |

### Adapters
Integration boards for existing equipment:

| Module | Cost | Description |
|--------|------|-------------|
| [Tank Sensor Adapter](adapters/tank-sensor-adapter/) | ~$25 | SeeLevel, Garnet, RV Whisper |
| [Heater Adapter](adapters/heater-adapter/) | ~$25 | Webasto, Espar, Chinese |
| [Generator Adapter](adapters/generator-adapter/) | ~$30 | Onan, Honda, Champion |
| [OBD-II Adapter](adapters/obd-ii-adapter/) | ~$35 | Vehicle diagnostics |

### 3D Printed Enclosures
All enclosures are parametric OpenSCAD designs:

| Enclosure | Description |
|-----------|-------------|
| [Cluster Box](enclosures/cluster-box/) | 4-node Pi housing |
| [HAT Stack Case](enclosures/hat-stack-case/) | Stackable HAT enclosure |
| [Dash Display Mount](enclosures/dash-display-mount/) | DIN/pod mount |
| [Camera Pods](enclosures/camera-pod-front/) | Front/rear/side/mini |
| [Router Enclosure](enclosures/router-enclosure/) | Antenna mount |
| [Sensor Box](enclosures/sensor-box/) | Exterior sensor housing |
| [Control Panel](enclosures/control-panel/) | Switch/button panel |
| [Antenna Mount](enclosures/antenna-mount/) | Roof antenna mount |

## Common Design Standards

### PCB Specifications
- **Form Factor**: Raspberry Pi HAT (65mm x 56.5mm)
- **Layers**: 2-layer (4-layer for RF/power)
- **Mounting**: M2.5 holes at HAT standard positions
- **Power**: 5V via Pi GPIO or 12V external
- **ESD Protection**: TVS diodes on all external interfaces

### Component Selection
- Prefer through-hole for DIY builds
- SMD alternatives noted for production
- Common footprints (0805, SOIC)
- Single-source parts avoided

### Connectors
- JST-XH for internal wiring
- Screw terminals for power
- RJ45 for sensor buses
- SMA for antennas
- USB-C where appropriate

## Master BOM

See [MASTER-BOM.csv](MASTER-BOM.csv) for complete system bill of materials with:
- DigiKey part numbers
- Mouser alternatives
- AliExpress links for budget builds
- DIY equivalent components

## Tools Required

### Buy Path (Minimal)
- Soldering iron (for headers)
- Screwdrivers
- Wire strippers/crimpers
- Multimeter

### Build Path (Full DIY)
- Soldering station with hot air
- SMD rework tools
- Oscilloscope (for debugging)
- Bench power supply
- PCB fabrication (or order from JLCPCB/PCBWay)

## Getting Started

1. **Choose your modules** based on your vehicle needs
2. **Decide buy vs build** for each component
3. **Order parts** from BOM or source alternatives
4. **Fabricate PCBs** (Gerbers provided)
5. **Assemble and test** following module guides
6. **Print enclosures** using provided STL/SCAD files
7. **Install and configure** with OpenRoam software

## File Structure

Each module follows this structure:
```
module-name/
├── README.md           # Overview, specs, buy/build options
├── bom/
│   ├── module-bom.csv  # Standard BOM (buy path)
│   └── diy-bom.csv     # Full DIY BOM (build path)
├── kicad/
│   ├── module.kicad_pro
│   ├── module.kicad_sch
│   └── module.kicad_pcb
├── firmware/
│   ├── src/
│   └── platformio.ini
└── docs/
    ├── MODULE-SPECS.md
    └── BUILD-FROM-SCRATCH.md
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for hardware contribution guidelines.

## License

CERN Open Hardware License v2 - Strongly Reciprocal (CERN-OHL-S-2.0)
