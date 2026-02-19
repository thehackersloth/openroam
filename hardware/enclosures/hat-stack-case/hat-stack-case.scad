// OpenRoam HAT Stack Case
// Stackable enclosure for Raspberry Pi with HATs
// License: CERN-OHL-S-2.0

/* [Pi Model] */
// Pi model (0=Pi4, 1=Pi5)
pi_model = 0;

/* [HAT Configuration] */
// Number of HATs stacked
num_hats = 1;
// HAT height (mm)
hat_height = 15;
// Extra clearance above HAT
hat_clearance = 3;

/* [Enclosure] */
// Wall thickness
wall = 2;
// Include ventilation
vented = true;
// Stackable design
stackable = true;

/* [Ports] */
// GPIO access slot
gpio_slot = true;
// SD card access
sd_access = true;
// Full USB/Ethernet exposure
port_exposure = true;

// Pi 4/5 board dimensions
board_width = 85;
board_length = 56;
board_thickness = 1.5;

// Mounting holes (from corner)
mount_x = 3.5;
mount_y = 3.5;
mount_spacing_x = 58;
mount_spacing_y = 49;

// Calculated
total_height = 5 + board_thickness + (num_hats * (hat_height + 2)) + hat_clearance + wall;
inner_width = board_width + 2;
inner_length = board_length + 2;
outer_width = inner_width + wall * 2;
outer_length = inner_length + wall * 2;

module vent_grid(w, h, slot_w, slot_h, spacing) {
    cols = floor((w - 5) / (slot_w + spacing));
    rows = floor((h - 5) / (slot_h + spacing));

    for (i = [0:cols-1]) {
        for (j = [0:rows-1]) {
            translate([2.5 + i * (slot_w + spacing), 2.5 + j * (slot_h + spacing), 0])
                cube([slot_w, slot_h, wall + 2]);
        }
    }
}

module base() {
    difference() {
        union() {
            // Main shell
            difference() {
                cube([outer_width, outer_length, total_height]);

                // Inner cavity
                translate([wall, wall, wall])
                    cube([inner_width, inner_length, total_height]);
            }

            // Corner posts with screw holes
            for (x = [wall + mount_x, wall + mount_x + mount_spacing_x]) {
                for (y = [wall + mount_y, wall + mount_y + mount_spacing_y]) {
                    translate([x, y, wall])
                        cylinder(h=5, d=6, $fn=32);
                }
            }
        }

        // Mounting screw holes
        for (x = [wall + mount_x, wall + mount_x + mount_spacing_x]) {
            for (y = [wall + mount_y, wall + mount_y + mount_spacing_y]) {
                translate([x, y, -1])
                    cylinder(h=total_height + 2, d=2.7, $fn=32);
            }
        }

        // Port cutouts (USB/Ethernet side)
        if (port_exposure) {
            // USB ports
            translate([outer_width - wall - 1, wall + 7, wall + 3])
                cube([wall + 2, 32, 18]);
            // Ethernet
            translate([outer_width - wall - 1, wall + 42, wall + 3])
                cube([wall + 2, 16, 15]);
        }

        // Power/HDMI side
        translate([-1, wall + 7, wall + 3])
            cube([wall + 2, 12, 8]); // USB-C power
        translate([-1, wall + 22, wall + 3])
            cube([wall + 2, 8, 6]); // micro HDMI 1
        translate([-1, wall + 33, wall + 3])
            cube([wall + 2, 8, 6]); // micro HDMI 2

        // SD card slot
        if (sd_access) {
            translate([wall + 1, -1, wall])
                cube([14, wall + 2, 4]);
        }

        // GPIO slot in top
        if (gpio_slot) {
            translate([wall + 5, wall + 2, total_height - wall - 1])
                cube([55, 8, wall + 2]);
        }

        // Top vents
        if (vented) {
            translate([wall + 5, wall + 15, total_height - wall - 1])
                vent_grid(inner_width - 10, inner_length - 25, 3, 15, 3);
        }
    }

    // Stacking features
    if (stackable) {
        // Alignment pegs
        for (x = [5, outer_width - 5]) {
            for (y = [5, outer_length - 5]) {
                translate([x, y, total_height])
                    cylinder(h=3, d=4, $fn=32);
            }
        }
    }
}

module lid() {
    difference() {
        union() {
            cube([outer_width, outer_length, wall]);

            // Inner lip
            translate([wall + 0.3, wall + 0.3, wall])
                difference() {
                    cube([inner_width - 0.6, inner_length - 0.6, 2]);
                    translate([1, 1, -1])
                        cube([inner_width - 2.6, inner_length - 2.6, 4]);
                }
        }

        // GPIO slot
        if (gpio_slot) {
            translate([wall + 5, wall + 2, -1])
                cube([55, 8, wall + 2]);
        }

        // Vents
        if (vented) {
            translate([wall + 5, wall + 15, -1])
                vent_grid(inner_width - 10, inner_length - 25, 3, 15, 3);
        }

        // Screw holes
        for (x = [wall + mount_x, wall + mount_x + mount_spacing_x]) {
            for (y = [wall + mount_y, wall + mount_y + mount_spacing_y]) {
                translate([x, y, -1])
                    cylinder(h=wall + 4, d=3.2, $fn=32);
                // Countersink
                translate([x, y, wall - 1])
                    cylinder(h=2, d=6, $fn=32);
            }
        }

        // Stacking alignment holes
        if (stackable) {
            for (x = [5, outer_width - 5]) {
                for (y = [5, outer_length - 5]) {
                    translate([x, y, -1])
                        cylinder(h=wall + 2, d=4.2, $fn=32);
                }
            }
        }
    }
}

// Render
base();
translate([outer_width + 10, 0, 0])
    lid();
