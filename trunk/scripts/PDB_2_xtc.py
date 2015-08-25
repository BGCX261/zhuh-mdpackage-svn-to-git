#!/usr/bin/env python
"""
MDAnalysis example: Convert Amber formatted trajectory to DCD
=============================================================

This example shows how one can use MDAnalysis to convert between
different trajectory formats.

"""

#from MDAnalysis.tests.datafiles import PRMpbc,TRJpbc_bz2
#from MDAnalysis.tests.datafiles import PRM,TRJ_bz2
from MDAnalysis import Universe, Writer
from MDAnalysis.core.util import greedy_splitext
from MDPackage import Simple_atom

import os.path
import sys

pdbfile =sys.argv[1] #PRMpbc
#intrj =sys.argv[2] #TRJpbc_bz2
ext = '.xtc'   # output format determined by extension

root, oldext = greedy_splitext(os.path.basename(pdbfile))
outtrj = root + ext
outpdb = root + '_new.pdb'

u = Universe(pdbfile,)

# create a writer instance for the output trajectory
w = Writer(outtrj, u.trajectory.numatoms)
aa=Simple_atom.Get_Simple_atom_list(pdbfile)
NUM_FRAMES=len(aa)/u.trajectory.numatoms
# loop through the trajectory and write a frame for every step
ts = u.trajectory[0]
for i in range(NUM_FRAMES):
    for j in range(u.trajectory.numatoms):
        ts._x[j]=aa[i*u.trajectory.numatoms+j].atom_coor_x*10
        ts._y[j]=aa[i*u.trajectory.numatoms+j].atom_coor_y*10
        ts._z[j]=aa[i*u.trajectory.numatoms+j].atom_coor_z*10
    w.write(ts)
    print "Converted frame %d" %(i+1)
w.close_trajectory()
print "Converted %r --> %r" % (pdbfile, outtrj)

# make a pdb file as a simple 'topology'
u.trajectory.rewind()
u.atoms.write(outpdb)
print "Created %r to be used with the trajectory" % outpdb
