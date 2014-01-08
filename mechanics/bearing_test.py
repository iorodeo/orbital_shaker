from __future__ import print_function
from py2scad import *

num_test = 10 
bearing_diam = 0.5*INCH2MM
hole_step = 0.005*INCH2MM

x = 0.9*num_test*INCH2MM 
y = 1.0*INCH2MM
z = 6.0
radius = 0.25*INCH2MM

hole_list = []

for i in range(0,num_test):
    x_pos = -0.5*x + (1+i)*1.5*bearing_diam
    y_pos = 0.0
    hole_diam = bearing_diam - i*hole_step
    print(i,hole_diam, hole_diam/INCH2MM)
    hole = (x_pos, y_pos, hole_diam)
    hole_list.append(hole)


plate = plate_w_holes(x,y,z,holes=hole_list, radius=radius)

prog = SCAD_Prog()
prog.fn = 50
prog.add(Projection(plate))
prog.write('bearing_test.scad')
