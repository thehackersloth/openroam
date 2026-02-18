# Contributing to OpenRoam

Thank you for your interest in contributing to OpenRoam! This project aims to make mobile living smarter and more connected through open-source hardware and software.

## Ways to Contribute

### Hardware
- Design new HAT modules or interface boards
- Improve existing PCB designs
- Add alternative "build from scratch" options for modules
- Create 3D printable enclosures
- Test and validate designs
- Write assembly documentation

### Software
- Improve the dashboard UI/UX
- Add new integrations (power systems, appliances, services)
- Write device drivers for HATs
- Optimize performance
- Fix bugs
- Add tests

### Documentation
- Write tutorials and guides
- Improve API documentation
- Create wiring diagrams
- Document vehicle-specific installations
- Translate to other languages

### Community
- Answer questions in Discussions
- Share your build photos and experiences
- Report bugs and suggest features

## Getting Started

### Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/openroam.git
cd openroam
```

### Set Up Development Environment

**Dashboard:**
```bash
cd software/openroam-dashboard
npm install
npm run dev
```

**Python Core:**
```bash
cd software/openroam-core
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

**Hardware (KiCad):**
- Install KiCad 7.0+
- Open project files in `hardware/*/kicad/`

## Hardware Contribution Guidelines

### Design Philosophy: Buy or Build

OpenRoam embraces the maker spirit. Every hardware module should offer:

1. **Buy Option**: Pre-made modules for quick assembly
   - List specific part numbers (DigiKey, Mouser, etc.)
   - Include module pinouts and integration details

2. **Build Option**: Full DIY from discrete components
   - Provide complete schematics
   - List all individual components
   - Include theory of operation

**Example - GPS Module:**
```
## GPS Receiver

### Option A: Buy Pre-Made Module
- u-blox MAX-M10S module ($18.50, DigiKey: 1909-MAX-M10S-ND)
- Simply connect VCC, GND, TX, RX

### Option B: Build from Scratch
For the ultimate DIY experience:
- GPS RF front-end IC (MAX2769)
- Correlator/baseband processor
- TCXO reference oscillator
- LNA and SAW filter
- Patch antenna design files included

See docs/BUILD-GPS-FROM-SCRATCH.md for complete guide.
```

### PCB Design Standards

- **Software**: KiCad 7.0+
- **Form Factor**: Raspberry Pi HAT standard (65mm x 56.5mm) where applicable
- **Layers**: 2-layer preferred, 4-layer when necessary
- **Mounting**: M2.5 holes at Pi HAT standard positions
- **Connectors**: Use common, readily available connectors
- **Silkscreen**: Include component values, polarity marks, version

### BOM Requirements

Every module BOM must include:
- Manufacturer part number
- DigiKey/Mouser part number
- Description
- Quantity
- Unit price
- Alternatives (especially open-source or DIY options)

### File Structure
```
module-name/
├── README.md           # Overview, buy/build options, specifications
├── bom/
│   ├── module-bom.csv  # Standard BOM
│   └── diy-bom.csv     # Full DIY component list
├── kicad/
│   ├── module.kicad_pro
│   ├── module.kicad_sch
│   └── module.kicad_pcb
├── firmware/
│   ├── src/
│   └── platformio.ini
└── docs/
    ├── MODULE-SPECS.md
    └── BUILD-FROM-SCRATCH.md  # Full DIY guide when applicable
```

## Software Contribution Guidelines

### Code Style

**TypeScript/Svelte:**
- Use Prettier with project config
- Follow existing patterns in codebase
- Type everything

**Python:**
- Follow PEP 8
- Use type hints
- Format with Black

### Commit Messages

Use conventional commits:
```
feat: add diesel heater control to climate page
fix: correct tank level calculation for capacitive sensors
docs: add wiring guide for Victron integration
```

### Testing

- Add tests for new features
- Ensure existing tests pass
- Test on actual hardware when possible

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Update documentation as needed
4. Run tests and linting
5. Submit PR with clear description
6. Address review feedback

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn
- Keep discussions on-topic

## Questions?

- Open a Discussion for general questions
- Open an Issue for bugs or feature requests
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under:
- MIT License for software
- CERN-OHL-S-2.0 for hardware
