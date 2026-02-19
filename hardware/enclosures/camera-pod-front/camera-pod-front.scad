// OpenRoam Camera Pod - Front
// Aerodynamic front-facing camera housing for parking/dashcam
// License: CERN-OHL-S-2.0

/* [Camera Module] */
// Camera type (0=IMX219, 1=IMX477, 2=IMX708)
camera_type = 0;
// Camera board width
cam_width = 25;
// Camera board height
cam_height = 24;
// Lens diameter
lens_dia = 8;

/* [Enclosure] */
// Wall thickness
wall = 2;
// Aerodynamic angle (degrees)
aero_angle = 15;
// Hood length (sun shade)
hood_length = 10;

/* [Mounting] */
// Mount type (0=adhesive, 1=screw, 2=suction)
mount_type = 1;
// Pivot angle range
pivot_range = 30;

/* [Cable] */
// Cable exit (0=back, 1=bottom)
cable_exit = 0;
// Cable gland diameter
cable_dia = 8;

/* [Lens Heater] */
// Include heater ring recess
lens_heater = false;
// Heater ring diameter
heater_dia = 15;

// Calculated dimensions
body_width = cam_width + wall * 2 + 4;
body_height = cam_height + wall * 2 + 4;
body_depth = 20;

module camera_body() {
    difference() {
        union() {
            // Main body with aerodynamic slope
            hull() {
                // Back face
                translate([0, 0, 0])
                    cube([body_width, body_height, 1]);
                // Front face (smaller, tilted)
                translate([wall, wall, body_depth])
                    rotate([aero_angle, 0, 0])
                        cube([body_width - wall*2, body_height - wall*2, 1]);
            }

            // Sun hood
            if (hood_length > 0) {
                translate([body_width/2, body_height/2, body_depth]) {
                    rotate([aero_angle, 0, 0])
                        hood();
                }
            }
        }

        // Internal cavity
        translate([wall, wall, wall])
            cube([cam_width + 4, cam_height + 4, body_depth]);

        // Lens opening
        translate([body_width/2, body_height/2, body_depth - 5])
            rotate([aero_angle, 0, 0])
                cylinder(h=20, d=lens_dia + 2, $fn=32);

        // Lens heater recess
        if (lens_heater) {
            translate([body_width/2, body_height/2, body_depth - 2])
                rotate([aero_angle, 0, 0])
                    cylinder(h=3, d=heater_dia, $fn=32);
        }

        // Cable exit
        if (cable_exit == 0) {
            // Back exit
            translate([body_width/2, body_height/2, -1])
                cylinder(h=wall+2, d=cable_dia, $fn=32);
        } else {
            // Bottom exit
            translate([body_width/2, -1, body_depth/2])
                rotate([-90, 0, 0])
                    cylinder(h=wall+2, d=cable_dia, $fn=32);
        }
    }

    // Camera mounting posts
    cam_offset_x = (body_width - cam_width) / 2;
    cam_offset_y = (body_height - cam_height) / 2;

    // IMX219 mounting holes: 21mm x 12.5mm
    for (x = [cam_offset_x + 2, cam_offset_x + 2 + 21]) {
        for (y = [cam_offset_y + 5.75, cam_offset_y + 5.75 + 12.5]) {
            translate([x, y, wall])
                camera_standoff(4);
        }
    }
}

module hood() {
    difference() {
        hull() {
            cylinder(h=1, d=lens_dia + 6, $fn=32);
            translate([0, 0, hood_length])
                scale([1.3, 1.3, 1])
                    cylinder(h=1, d=lens_dia + 6, $fn=32);
        }
        translate([0, 0, -1])
            cylinder(h=hood_length + 3, d=lens_dia + 2, $fn=32);
    }
}

module camera_standoff(h) {
    difference() {
        cylinder(h=h, d=4, $fn=32);
        cylinder(h=h+1, d=2.2, $fn=32);
    }
}

module back_plate() {
    difference() {
        cube([body_width, body_height, wall]);

        // Cable hole
        translate([body_width/2, body_height/2, -1])
            cylinder(h=wall+2, d=cable_dia, $fn=32);

        // Screw holes
        for (x = [5, body_width - 5]) {
            for (y = [5, body_height - 5]) {
                translate([x, y, -1])
                    cylinder(h=wall+2, d=3, $fn=32);
            }
        }
    }
}

module mount_bracket() {
    if (mount_type == 1) {
        // Screw mount bracket
        difference() {
            union() {
                cube([body_width, 15, 3]);
                translate([0, 0, 0])
                    cube([body_width, 3, 15]);
            }
            // Mounting holes
            for (x = [10, body_width - 10]) {
                translate([x, 7.5, -1])
                    cylinder(h=5, d=4, $fn=32);
            }
            // Pivot slot
            translate([body_width/2, -1, 10])
                rotate([-90, 0, 0])
                    cylinder(h=5, d=5, $fn=32);
        }
    }
}

// Render parts
camera_body();

translate([0, body_height + 10, 0])
    back_plate();

translate([0, -25, 0])
    mount_bracket();
