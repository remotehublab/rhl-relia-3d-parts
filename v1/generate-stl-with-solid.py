import os
import math
from solid import *
from solid.utils import *

# Dimensions of the cuboid
width = 22.2  # cm; max. 9.5 in (241.3 mm)
length = 30.2  # cm; max 13.58 in (344 mm)
height = 7.2  # cm; min 2.15 in (54 mm)

# Thickness of the walls
thickness = 0.4  # cm

text_height = 0.1 # cm

text_size = 3

# Diameter of the holes in the bottom
big_hole_diameter = 2  # cm

phase_dock_hole_diameter = 0.955 # cm (phase dock main hole pattern)

def create_relia_surface(width, length, height, thickness):
    # Outer cuboid
#    outer = cube([width, length, height])

    corner_radius = thickness
    corner = cylinder(h=height, r=corner_radius, segments=32)
    corners = [
        translate([corner_radius, corner_radius, 0])(corner),
        translate([width - corner_radius, corner_radius, 0])(corner),
        translate([corner_radius, length - corner_radius, 0])(corner),
        translate([width - corner_radius, length - corner_radius, 0])(corner)
    ]

    # Hull around the corners to create rounded edges
    rounded_cube = hull()(corners)


    # Inner cuboid, subtracted from outer to create walls
#    inner = translate([thickness, thickness, thickness])(  # small offset to ensure complete subtraction
#        cube([width - 2 * thickness, length - 2 * thickness, height - thickness])
#    )

    # Size of the inner cuboid
    inner_width = width - 2 * thickness
    inner_length = length - 2 * thickness
    inner_height = height - thickness

    # Create cylinders at each corner
    corner = cylinder(h=inner_height, r=corner_radius, segments=32)
    corners = [
        translate([corner_radius, corner_radius, 0])(corner),
        translate([inner_width - corner_radius, corner_radius, 0])(corner),
        translate([corner_radius, inner_length - corner_radius, 0])(corner),
        translate([inner_width - corner_radius, inner_length - corner_radius, 0])(corner)
    ]

    # Hull around the corners to create rounded edges
    rounded_inner = hull()(corners)

    # Translate the inner cuboid to its correct position
    inner = translate([thickness, thickness, thickness])(rounded_inner)

    holes = []

    # cabling_hole = cube([2, 8, thickness])

    # Create cylinders at each corner
    cabling_hole_width = 2
    cabling_hole_length = 8
    corner = cylinder(h=thickness, r=corner_radius, segments=32)
    corners = [
        translate([corner_radius, corner_radius, 0])(corner),
        translate([cabling_hole_width - corner_radius, corner_radius, 0])(corner),
        translate([corner_radius, cabling_hole_length - corner_radius, 0])(corner),
        translate([cabling_hole_width - corner_radius, cabling_hole_length - corner_radius, 0])(corner)
    ]

    # Hull around the corners to create rounded edges
    cabling_hole = hull()(corners)

    holes.append(translate([thickness, thickness + 4, 0])(cabling_hole))
    holes.append(translate([thickness, thickness + 4 + 8 + 5.4, 0])(cabling_hole))

    miniwalls = []

    lateral_wall = cube([14, thickness, 1.5])

    # Outside walls
    exterior_wall_to_cabling_hole = abs(8 - 8.25 - thickness)
    miniwalls.append(translate([thickness + 2, thickness + 4 - exterior_wall_to_cabling_hole, thickness])(lateral_wall))
    miniwalls.append(translate([thickness + 2, thickness + 4 + 8 + 5.4 + 8 + exterior_wall_to_cabling_hole, thickness])(lateral_wall))

    # Inside walls
    miniwalls.append(translate([thickness + 2, thickness + 4 + 8, thickness])(lateral_wall))
    miniwalls.append(translate([thickness + 2, thickness + 4 + 8 + 5.4 - thickness, thickness])(lateral_wall))

    upper_wall = cube([thickness, thickness + 1.5, 1.5])

    miniwalls.append(translate([thickness + 2 + 14, thickness + 4 - exterior_wall_to_cabling_hole, thickness])(upper_wall))
    miniwalls.append(translate([thickness + 2 + 14, thickness + 4 + 8 - 1.5, thickness])(upper_wall))


    miniwalls.append(translate([thickness + 2 + 14, thickness + 4 + 8 + 5.4 - thickness, thickness])(upper_wall))
    miniwalls.append(translate([thickness + 2 + 14, thickness + 4 + 8 + 5.4 + 8 + exterior_wall_to_cabling_hole - 1.5, thickness])(upper_wall))

    # Creating holes in the bottom face
    # big_hole = cylinder(d=big_hole_diameter, h=height + 0.2, segments=32)

    phase_dock_hole = cylinder(d=phase_dock_hole_diameter, h=height + 0.2, segments=32)
    phase_dock_hole_smaller = cylinder(d=phase_dock_hole_diameter / 2, h=height + 0.2, segments=32)
    

    # holes.append(translate([15, 15, 0])(big_hole))
    # holes.append(translate([5, 5, 0])(big_hole))

    # Small holes (phasedock alignment and zipties)    
    holes.append(translate([thickness + 2 + 2 + 2.5 * 0, 1 + 2.5 * 0, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 1, 1 + 2.5 * 0, 0])(phase_dock_hole))

    holes.append(translate([thickness + 2 + 2 + 2.5 * 0, 1 + 2.5 * 1, 0])(phase_dock_hole_smaller))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 1, 1 + 2.5 * 1, 0])(phase_dock_hole_smaller))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 2, 1 + 2.5 * 1, 0])(phase_dock_hole_smaller))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 3, 1 + 2.5 * 1, 0])(phase_dock_hole_smaller))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 4, 1 + 2.5 * 1, 0])(phase_dock_hole_smaller))

    holes.append(translate([thickness + 2 + 2 + 2.5 * 0, 1 + 2.5 * 5, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 1, 1 + 2.5 * 5, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 2, 1 + 2.5 * 5, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 3, 1 + 2.5 * 5, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 4, 1 + 2.5 * 5, 0])(phase_dock_hole))

    holes.append(translate([thickness + 2 + 2 + 2.5 * 0, 1 + 2.5 * 6, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 1, 1 + 2.5 * 6, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 2, 1 + 2.5 * 6, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 3, 1 + 2.5 * 6, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 4, 1 + 2.5 * 6, 0])(phase_dock_hole))

    holes.append(translate([thickness + 2 + 2 + 2.5 * 0, 1 + 2.5 * 11, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 1, 1 + 2.5 * 11, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 2, 1 + 2.5 * 11, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 3, 1 + 2.5 * 11, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 4, 1 + 2.5 * 11, 0])(phase_dock_hole))

    holes.append(translate([thickness + 2 + 2 + 2.5 * 6, 1 + 2.5 * 0, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 5, 1 + 2.5 * 0, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 6, 1 + 2.5 * 1, 0])(phase_dock_hole))

    holes.append(translate([thickness + 2 + 2 + 2.5 * 6, 1 + 2.5 * 11, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 5, 1 + 2.5 * 11, 0])(phase_dock_hole))
    holes.append(translate([thickness + 2 + 2 + 2.5 * 6, 1 + 2.5 * 10, 0])(phase_dock_hole))


    tx_text = text("Tx", size=text_size, font="Arial", halign="center", valign="top")
    rx_text = text("Rx", size=text_size, font="Arial", halign="center", valign="top")

    extruded_tx_text = linear_extrude(height=text_height)(tx_text)
    extruded_rx_text = linear_extrude(height=text_height)(rx_text)

    rx_text_position = translate([thickness + 2 + 14/2, thickness + 4 + 8 + 5.4 + 8/2, thickness - text_height])(rotate([0, 0, 270])(extruded_rx_text))

    tx_text_position = translate([thickness + 2 + 14/2, thickness + 4 + 8/2, thickness - text_height])(rotate([0, 0, 270])(extruded_tx_text))

    texts = [ tx_text_position, rx_text_position ]

#    return outer - inner - union()(*holes) + union()(*miniwalls) - union()(*texts)
    return rounded_cube - inner - union()(*holes) + union()(*miniwalls) - union()(*texts)

# Create the model
model = create_relia_surface(width, length, height, thickness)

# Exporting the model to STL
file_out = 'cuboid_with_holes.scad'
file_stl = 'cuboid_with_holes.stl'

if os.path.exists(file_out):
    os.remove(file_out)

if os.path.exists(file_stl):
    os.remove(file_stl)

scad_render_to_file(model, file_out)

from subprocess import run

run(["openscad", "-o",  file_stl, file_out])
run(["f3d", file_stl])
