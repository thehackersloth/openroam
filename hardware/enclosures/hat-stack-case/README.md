# HAT Stack Case

Stackable enclosure for Raspberry Pi 4/5 with HAT modules.

## Features

- Fits Pi 4 or Pi 5
- Accommodates 1-3 stacked HATs
- Ventilated top and sides
- GPIO access slot
- Full port exposure (USB, Ethernet, HDMI, power)
- Stackable for multi-node setups
- SD card access

## Specifications

| Parameter | Value |
|-----------|-------|
| External Dimensions | ~93 x 64 x varies |
| Height (1 HAT) | ~35mm |
| Height (2 HATs) | ~52mm |
| Height (3 HATs) | ~69mm |
| Material | PETG recommended |

## Print Settings

| Setting | Value |
|---------|-------|
| Layer Height | 0.2mm |
| Infill | 20% |
| Perimeters | 3 |
| Material | PETG |
| Supports | No |
| Orientation | As designed |

## Hardware Required

| Item | Quantity | Notes |
|------|----------|-------|
| M2.5 x 12mm standoffs | 4 | Between Pi and HAT |
| M2.5 x 6mm screws | 8 | Pi mounting |
| M2.5 nuts or inserts | 4 | Optional for lid |

## Assembly

1. Insert Pi into base, align with mounting posts
2. Secure Pi with M2.5 screws from bottom
3. Install HAT standoffs
4. Mount HAT(s)
5. Attach lid with screws

## Stacking

Cases can be stacked for multi-node clusters:
1. Align stacking pegs with holes
2. Cases lock together without hardware
3. Use M3 threaded rods through corners for secure stack

## Customization

```openscad
pi_model = 0;       // 0=Pi4, 1=Pi5
num_hats = 1;       // Number of HATs (1-3)
hat_height = 15;    // Height of each HAT
vented = true;      // Enable ventilation
stackable = true;   // Include stacking features
gpio_slot = true;   // GPIO access in lid
```

## STL Files

- `hat-stack-case-1hat.stl` - Base for 1 HAT
- `hat-stack-case-2hat.stl` - Base for 2 HATs
- `hat-stack-case-3hat.stl` - Base for 3 HATs
- `hat-stack-case-lid.stl` - Universal lid
