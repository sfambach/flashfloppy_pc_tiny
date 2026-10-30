// Spacers for the Mini Floppy Emulator (main PCB + cover PCB).
// Measured by Stefan: gap between boards 11 mm, mounting holes about 3 mm.
// Assumed: PCB thickness 1.6 mm. All values in mm.

part = "screw_spacer"; // [screw_spacer, snap_sleeve, snap_pin]

gap       = 11.0;  // distance between the boards
pcb       = 1.6;   // board thickness (assumed)
hole      = 3.0;   // board hole
od        = 6.0;   // outer diameter of spacer / sleeve

// Variant A: spacer, M3 screws from both sides cut their own thread
screw_core = 2.6;  // pilot bore for M3 self-cutting into plastic

// Variant B: sleeve with snap pins from top and bottom
lip_len   = 2.0;   // catch lip at each sleeve end
lip_d     = 2.9;   // lip bore (shank passes, barb snaps behind)
mid_d     = 3.6;   // wide bore in the middle
head_d    = 6.0;   // pin head diameter
head_h    = 1.2;   // pin head height
shank_d   = 2.8;   // pin shank, fits the 3 mm board hole
barb_d    = 3.4;   // barb diameter, snaps behind the lip
barb_len  = 1.8;   // barb length
slot_w    = 0.8;   // slot that lets the barb compress
slot_len  = 4.0;   // slot length from the tip

$fn = 64;

module screw_spacer() {
    difference() {
        cylinder(d = od, h = gap);
        translate([0, 0, -1]) cylinder(d = screw_core, h = gap + 2);
        // small entry chamfers so the screw starts straight
        translate([0, 0, -0.01]) cylinder(d1 = screw_core + 0.8, d2 = screw_core, h = 0.4);
        translate([0, 0, gap - 0.39]) cylinder(d1 = screw_core, d2 = screw_core + 0.8, h = 0.4);
    }
}

module snap_sleeve() {
    difference() {
        cylinder(d = od, h = gap);
        translate([0, 0, -1]) cylinder(d = lip_d, h = gap + 2);
        translate([0, 0, lip_len]) cylinder(d = mid_d, h = gap - 2 * lip_len);
        // entry chamfers guide the barb into the lip
        translate([0, 0, -0.01]) cylinder(d1 = lip_d + 0.6, d2 = lip_d, h = 0.3);
        translate([0, 0, gap - 0.29]) cylinder(d1 = lip_d, d2 = lip_d + 0.6, h = 0.3);
    }
}

// Pin printed head down. Shank length = board + lip (+play), so the barb sits
// just behind the lip when the head rests on the board.
module snap_pin() {
    shank_len = pcb + lip_len + 0.1; // 0.1 play so the barb clears the lip
    tip = 0.6;
    difference() {
        union() {
            cylinder(d = head_d, h = head_h);
            translate([0, 0, head_h]) cylinder(d = shank_d, h = shank_len);
            translate([0, 0, head_h + shank_len]) cylinder(d = barb_d, h = barb_len - tip);
            translate([0, 0, head_h + shank_len + barb_len - tip]) cylinder(d1 = barb_d, d2 = shank_d - 0.6, h = tip);
        }
        translate([-slot_w / 2, -od, head_h + shank_len + barb_len - slot_len]) cube([slot_w, 2 * od, slot_len + 1]);
    }
}

if (part == "screw_spacer") screw_spacer();
if (part == "snap_sleeve")  snap_sleeve();
if (part == "snap_pin")     snap_pin();
