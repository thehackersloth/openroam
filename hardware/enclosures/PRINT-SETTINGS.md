# OpenRoam Enclosure Print Settings

## Quick Reference

| Enclosure | Material | Infill | Perimeters | Supports | Time | Filament |
|-----------|----------|--------|------------|----------|------|----------|
| cluster-box | PETG/ASA | 25% | 4 | No | 10h | 150g |
| hat-stack-case | PETG | 20% | 3 | No | 2h | 40g |
| dash-display-mount | ASA | 30% | 4 | Yes | 4h | 80g |
| camera-pod-front | ASA | 25% | 4 | Yes | 1.5h | 25g |
| camera-pod-rear | ASA | 25% | 4 | Yes | 2h | 35g |
| camera-pod-side | ASA | 25% | 4 | Yes | 1.5h | 25g |
| camera-pod-mini | PETG | 30% | 3 | No | 30m | 10g |
| router-enclosure | ASA | 25% | 4 | No | 3h | 60g |
| sensor-box | ASA | 20% | 4 | No | 1h | 20g |
| control-panel | PETG | 20% | 3 | No | 2h | 35g |
| antenna-mount | ASA | 40% | 4 | Yes | 2h | 50g |

## Material Selection

### Indoor Use
- **PETG** - Best all-around choice
  - Temperature resistant to 70°C
  - Easy to print, minimal warping
  - Good layer adhesion

### Outdoor/Vehicle Use
- **ASA** - Recommended for exterior
  - UV resistant (critical for vehicle use)
  - Temperature resistant to 95°C
  - Weather resistant
  - Requires enclosure to print well

### High-Temperature (Engine Bay)
- **ABS** or **PC** - For engine compartment
  - Temperature resistant to 100°C+
  - Requires enclosure and heated bed
  - Post-process with acetone vapor for water resistance

## Detailed Print Profiles

### Standard PETG Profile
```
Layer Height: 0.2mm
First Layer Height: 0.25mm
Perimeters: 3
Top Layers: 4
Bottom Layers: 4
Infill: 20%
Infill Pattern: Gyroid
Nozzle Temp: 235°C
Bed Temp: 80°C
Speed: 50mm/s
Cooling: 50-80%
```

### Standard ASA Profile
```
Layer Height: 0.2mm
First Layer Height: 0.25mm
Perimeters: 4
Top Layers: 5
Bottom Layers: 5
Infill: 25%
Infill Pattern: Gyroid
Nozzle Temp: 250°C
Bed Temp: 100°C
Speed: 40mm/s
Cooling: 0-30% (enclosed)
Enclosure Temp: 40-50°C
```

### Structural Parts Profile
For mounting brackets, antenna mounts, DIN clips:
```
Layer Height: 0.2mm
Perimeters: 5
Infill: 40%
Infill Pattern: Cubic
```

## Weatherproofing

For outdoor enclosures:

1. **Print Settings**
   - Use 4+ perimeters
   - 100% infill on top/bottom
   - No gaps in walls

2. **Post-Processing**
   - Sand mating surfaces to 400 grit
   - Apply silicone gasket or foam tape
   - Use automotive-grade RTV silicone on seams

3. **Hardware**
   - Stainless steel screws only
   - Use O-rings on cable glands
   - Conformal coat PCBs inside

## Heat-Set Inserts

All enclosures use brass heat-set inserts:

| Thread | Insert OD | Hole Size | Depth |
|--------|-----------|-----------|-------|
| M2 | 3.2mm | 3.0mm | 4mm |
| M2.5 | 3.8mm | 3.6mm | 5mm |
| M3 | 4.6mm | 4.4mm | 6mm |
| M4 | 5.6mm | 5.4mm | 7mm |

**Installation:**
1. Heat soldering iron to 220°C (for PETG) or 250°C (for ASA)
2. Place insert on hole
3. Press straight down with iron tip
4. Insert should be flush or 0.5mm below surface
5. Let cool before use

## Troubleshooting

### Warping
- Increase bed temp by 5°C
- Use brim (5-10mm)
- Check for drafts
- Use enclosure for ASA/ABS

### Layer Separation
- Increase nozzle temp by 5-10°C
- Reduce cooling
- Check for moisture in filament
- Dry filament before use

### Weak Parts
- Increase perimeters
- Increase infill
- Check layer adhesion
- Rotate part for better layer orientation
