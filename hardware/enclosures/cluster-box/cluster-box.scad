// OpenRoam Cluster Box
// 4-node Raspberry Pi cluster enclosure with ventilation and DIN rail mount
// License: CERN-OHL-S-2.0

/* [Board Configuration] */
// Number of Pi boards
num_boards = 4;
// Board width (Pi 4/5)
board_width = 85;
// Board length
board_length = 56;
// Board height including HAT
board_height = 25;
// Spacing between boards
board_spacing = 10;

/* [Enclosure] */
// Wall thickness
wall = 2.5;
// Corner radius
corner_radius = 3;
// Lid style (0=flat, 1=vented)
lid_style = 1;

/* [Ventilation] */
// Enable side vents
side_vents = true;
// Vent slot width
vent_width = 2;
// Vent slot spacing
vent_spacing = 4;
// Vent slot length
vent_length = 15;

/* [Mounting] */
// DIN rail mount
din_rail = true;
// Screw mount holes
screw_mount = true;
// Mount hole diameter
mount_hole_dia = 4;

/* [Calculated] */
inner_width = board_width + 10;
inner_length = (board_length * num_boards) + (board_spacing * (num_boards - 1)) + 10;
inner_height = board_height + 15;

outer_width = inner_width + (wall * 2);
outer_length = inner_length + (wall * 2);
outer_height = inner_height + (wall * 2);

module rounded_box(w, l, h, r) {
    hull() {
        for (x = [r, w-r]) {
            for (y = [r, l-r]) {
                translate([x, y, 0])
                    cylinder(h=h, r=r, $fn=32);
            }
        }
    }
}

module vent_slots(length, height, slot_w, slot_l, spacing) {
    num_slots = floor((height - 10) / (slot_w + spacing));
    for (i = [0:num_slots-1]) {
        translate([-1, (length - slot_l) / 2, 5 + i * (slot_w + spacing)])
            cube([wall + 2, slot_l, slot_w]);
    }
}

module pi_standoff(h) {
    difference() {
        cylinder(h=h, d=6, $fn=32);
        cylinder(h=h+1, d=2.5, $fn=32);
    }
}

module base() {
    difference() {
        // Outer shell
        rounded_box(outer_width, outer_length, outer_height - wall, corner_radius);

        // Inner cavity
        translate([wall, wall, wall])
            rounded_box(inner_width, inner_length, outer_height, corner_radius - 0.5);

        // Side vents
        if (side_vents) {
            // Left side
            translate([0, 0, 0])
                vent_slots(outer_length, outer_height, vent_width, vent_length, vent_spacing);
            // Right side
            translate([outer_width - wall, 0, 0])
                vent_slots(outer_length, outer_height, vent_width, vent_length, vent_spacing);
        }

        // Cable entry holes (USB, Ethernet, Power)
        // Front
        translate([outer_width/2 - 15, -1, wall + 5])
            cube([30, wall + 2, 12]);
        // Back
        translate([outer_width/2 - 20, outer_length - wall - 1, wall + 5])
            cube([40, wall + 2, 15]);
    }

    // Pi standoffs for each board
    for (i = [0:num_boards-1]) {
        board_y = wall + 5 + (i * (board_length + board_spacing));
        // Pi mounting holes are 58mm x 49mm
        for (x = [wall + 5, wall + 5 + 58]) {
            for (y = [board_y + 3.5, board_y + 3.5 + 49]) {
                translate([x, y, wall])
                    pi_standoff(5);
            }
        }
    }

    // DIN rail mount
    if (din_rail) {
        translate([outer_width/2, outer_length + 5, 0])
            din_rail_clip();
    }
}

module din_rail_clip() {
    // Standard 35mm DIN rail clip
    clip_width = 10;
    clip_depth = 8;
    rail_width = 35;

    translate([-rail_width/2 - clip_width, -clip_depth, 0]) {
        difference() {
            cube([rail_width + clip_width*2, clip_depth, 15]);
            // Rail channel
            translate([clip_width, -1, 7])
                cube([rail_width, clip_depth + 2, 9]);
            // Clip relief
            translate([clip_width - 2, clip_depth - 3, 7])
                cube([4, 4, 9]);
            translate([clip_width + rail_width - 2, clip_depth - 3, 7])
                cube([4, 4, 9]);
        }
    }
}

module lid() {
    difference() {
        union() {
            // Main lid
            rounded_box(outer_width, outer_length, wall, corner_radius);
            // Lip to fit inside base
            translate([wall + 0.2, wall + 0.2, -3])
                rounded_box(inner_width - 0.4, inner_length - 0.4, 3, corner_radius - 1);
        }

        // Vents in lid
        if (lid_style == 1) {
            for (i = [0:num_boards-1]) {
                board_y = wall + 5 + (i * (board_length + board_spacing));
                // Vent grid over each Pi
                for (x = [0:4]) {
                    for (y = [0:3]) {
                        translate([wall + 15 + x*12, board_y + 10 + y*10, -1])
                            cylinder(h=wall+2, d=8, $fn=6);
                    }
                }
            }
        }

        // Screw holes for lid
        for (x = [10, outer_width - 10]) {
            for (y = [10, outer_length/2, outer_length - 10]) {
                translate([x, y, -1])
                    cylinder(h=wall+2, d=3.2, $fn=32);
                translate([x, y, wall - 1.5])
                    cylinder(h=2, d=6, $fn=32);
            }
        }
    }
}

// Render
base();
translate([0, 0, outer_height + 10])
    lid();
