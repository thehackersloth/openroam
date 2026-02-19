# OpenRoam 3D Printed Enclosures

All enclosures are parametric OpenSCAD designs that can be customized for your specific hardware and mounting requirements.

## Enclosure Types

| Enclosure | Description | Recommended Material |
|-----------|-------------|---------------------|
| **cluster-box** | 4-node Pi cluster housing, ventilated, DIN rail mount | PETG or ASA |
| **hat-stack-case** | Stackable HAT enclosure, Pi 4/5 compatible | PETG |
| **dash-display-mount** | DIN-slot or pod mount for 7" display | ASA (UV resistant) |
| **camera-pod-front** | Aerodynamic front camera housing | ASA or ABS |
| **camera-pod-rear** | License plate area mount, IR illumination | ASA |
| **camera-pod-side** | Mirror/fender mount blind spot camera | ASA |
| **camera-pod-mini** | Compact 20mm cube camera housing | PETG |
| **router-enclosure** | External antenna mount, weatherproof | ASA |
| **sensor-box** | Exterior temp/humidity sensor housing | ASA |
| **control-panel** | Flush-mount switch/button panel | PETG |
| **antenna-mount** | Roof mount for cellular/WiFi/GPS antennas | ASA |

## Print Settings

### General Recommendations

| Setting | Value | Notes |
|---------|-------|-------|
| Layer Height | 0.2mm | 0.16mm for detailed parts |
| Infill | 20-30% | Higher for structural parts |
| Perimeters | 3-4 | More for weatherproof enclosures |
| Top/Bottom Layers | 4-5 | |
| Supports | As needed | Most designs minimize supports |

### Material Guide

| Material | Use Case | Properties |
|----------|----------|------------|
| **PLA** | Indoor prototypes only | Not heat/UV resistant |
| **PETG** | Indoor enclosures | Good strength, moderate heat resistance |
| **ASA** | Outdoor/vehicle | UV resistant, heat resistant to 95°C |
| **ABS** | Engine bay | Heat resistant but needs enclosure to print |

### Weatherproofing

For outdoor enclosures:
1. Print with ASA or UV-resistant PETG
2. Use 4+ perimeters for water resistance
3. Add silicone gaskets to seams
4. Use stainless steel hardware
5. Apply conformal coating to PCBs inside

## Customization

All OpenSCAD files use parametric design. Common parameters:

```openscad
// Board dimensions (adjust for your specific Pi model)
board_width = 85;
board_length = 56;
board_height = 17;  // Including HAT

// Wall thickness
wall = 2.5;

// Ventilation
vent_slots = true;
vent_width = 2;
vent_spacing = 4;

// Mounting
din_rail_mount = true;
screw_mount = true;
```

## Assembly

Most enclosures use:
- M2.5 or M3 brass heat-set inserts
- M2.5 or M3 stainless steel screws
- Nylon standoffs for PCB mounting

## STL Files

Pre-generated STL files for common configurations are in each enclosure's directory. For custom sizes, modify the OpenSCAD source and export.

## Contributing

When adding new enclosures:
1. Use parametric OpenSCAD design
2. Include print settings in README
3. Export STL for standard configurations
4. Test fit with actual hardware
5. Document any assembly notes
