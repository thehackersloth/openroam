# Cluster Box

4-node Raspberry Pi cluster enclosure with integrated ventilation and optional DIN rail mounting.

## Features

- Holds 4x Raspberry Pi 4/5 boards with HATs
- Passive ventilation slots on sides and lid
- DIN rail mount (standard 35mm rail)
- Cable routing channels
- Modular lid design

## Specifications

| Parameter | Value |
|-----------|-------|
| External Dimensions | ~105 x 275 x 50 mm |
| Internal Clearance | 25mm per board (with HAT) |
| Board Spacing | 10mm between boards |
| Wall Thickness | 2.5mm |
| Material | PETG or ASA recommended |

## Print Settings

| Setting | Base | Lid |
|---------|------|-----|
| Layer Height | 0.2mm | 0.2mm |
| Infill | 25% | 20% |
| Perimeters | 4 | 3 |
| Top/Bottom Layers | 5 | 4 |
| Supports | No | No |
| Orientation | As designed | Flip upside down |

**Print Time:** ~8-10 hours total (base + lid)
**Filament:** ~150g PETG

## Hardware Required

| Item | Quantity | Notes |
|------|----------|-------|
| M2.5 x 6mm screws | 16 | Pi mounting |
| M2.5 brass inserts | 16 | Heat-set into standoffs |
| M3 x 8mm screws | 6 | Lid attachment |
| M3 brass inserts | 6 | Heat-set into base |
| 40mm fan (optional) | 1-2 | 5V, mount in lid vents |

## Assembly

1. Insert M2.5 brass heat-set inserts into Pi standoffs
2. Insert M3 brass heat-set inserts into lid screw holes
3. Mount Pi boards with M2.5 screws
4. Route cables through front/back openings
5. Attach lid with M3 screws

## Customization

Edit `cluster-box.scad` parameters:

```openscad
num_boards = 4;      // Number of Pi boards (1-6)
board_height = 25;   // Adjust for HAT stack height
din_rail = true;     // Enable/disable DIN rail mount
side_vents = true;   // Enable/disable ventilation
```

## STL Files

- `cluster-box-base.stl` - Main enclosure body
- `cluster-box-lid.stl` - Vented lid
- `cluster-box-lid-solid.stl` - Solid lid (for fan mount)
