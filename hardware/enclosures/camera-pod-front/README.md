# Camera Pod - Front

Aerodynamic front-facing camera housing for parking assist and dashcam use.

## Features

- Aerodynamic profile to reduce wind noise
- Sun hood to prevent lens flare
- Optional lens heater ring for defrost
- Weatherproof design (IP65 with gasket)
- Adjustable mount bracket

## Specifications

| Parameter | Value |
|-----------|-------|
| Compatible Cameras | IMX219, IMX477, IMX708 |
| External Dimensions | ~35 x 32 x 30 mm |
| Mounting | Adhesive, screw, or suction |
| Cable Exit | Rear or bottom |
| Material | ASA recommended |

## Print Settings

| Setting | Value |
|---------|-------|
| Layer Height | 0.2mm |
| Infill | 25% |
| Perimeters | 4 |
| Material | ASA (UV resistant) |
| Supports | Yes (for hood overhang) |
| Orientation | Lens facing up |

## Hardware Required

| Item | Quantity | Notes |
|------|----------|-------|
| M2 x 4mm screws | 4 | Camera mounting |
| M3 x 8mm screws | 4 | Back plate |
| M3 brass inserts | 4 | Heat-set |
| Cable gland M8 | 1 | Weatherproof |
| Silicone gasket | 1 | Between body and plate |
| Lens heater ring | 1 | Optional, 12V |

## Mounting Options

### Grille Mount
Best for parking assist. Mount behind grille opening.

### Hood Mount
Use adhesive pad on flat section of hood.

### Bumper Mount
Screw mount to bumper cover (check for clearance behind).

## Wiring

- **Camera:** 15-pin FFC ribbon cable (custom length)
- **Heater:** 12V 0.5A (use with relay/MOSFET control)
- Route cables through existing grommets when possible

## Customization

```openscad
camera_type = 0;    // 0=IMX219, 1=IMX477, 2=IMX708
aero_angle = 15;    // Angle of front face
hood_length = 10;   // Sun shade length (0 to disable)
lens_heater = true; // Include heater ring recess
mount_type = 1;     // 0=adhesive, 1=screw, 2=suction
```

## STL Files

- `camera-pod-front-body.stl` - Main housing
- `camera-pod-front-back.stl` - Rear cover plate
- `camera-pod-front-mount.stl` - Mounting bracket
