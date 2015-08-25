#!/usr/bin/env python
"""
Trj_modify is used to fit the frames in trajectory to the first frame 
by trans and rot.
@change:
    - 2011.12.26.
        - Add those words.
        - Modified it.
"""

from MDAnalysis import Universe, Writer
from MDAnalysis.core.util import greedy_splitext

from MDPackage import Simple_atom
from MDPackage import usage
from MDPackage.mymath import least_squares_fitting
import os.path
import numpy
import sys
import time as Time

#import psyco ; psyco.jit() 
#from psyco.classes import *


def Usage():
    print "Usage: Trj_modify.py topfile trjfile output.xtc"

def Move_2_center(top_file,trj_file,trjout_file,skip=1):
    u=Universe(top_file,trj_file)
    TRAJ_FRAMES=u.trajectory.numframes
    atom_l=Simple_atom.Get_Simple_atom_list(top_file)

    while True:
        fit_residue=Simple_atom.Get_residue(top_file)
        if len(fit_residue) > 1:
            print "Only 1 residue is aviliable."
            continue
        else:
            break
    while True:
        fit_atom=Simple_atom.Get_atom(atom_l,fit_residue[0])
        if len(fit_atom) > 1:
            print "Only 1 atom is aviliable."
            continue
        else: 
            break

    fitting_group=Simple_atom.Get_residue(top_file)

    fit_atom=fit_atom[0]

    w = Writer(trjout_file, u.trajectory.numatoms)
    NUM_ATOMS=len(atom_l)

    print '''Note: this program will read the pbc condition and use the dimensions \
read from trajectory files. You should make sure the dimensions are right or \
it will create a wrong output trajectory file.'''

    START_TIME=Time.time()
    # loop through the trajectory and write a frame for every step
    for ts in u.trajectory:
        if ts.frame % skip != 1:
            break

        if ts.frame==1:
            label_coordinate=[ts._x[fit_atom],ts._y[fit_atom],ts._z[fit_atom]]

            # origin_list=list()
            # for atom in atom_l:
            #     if atom.residue_serial in fitting_group:
            #         origin_list.append([\
            #                 ts._x[atom_l.index(atom)],\
            #                 ts._y[atom_l.index(atom)],\
            #                 ts._z[atom_l.index(atom)],\
            #                 ])

        else:
            shift=[label_coordinate[0]-ts._x[fit_atom],\
                    label_coordinate[1]-ts._y[fit_atom],\
                    label_coordinate[2]-ts._z[fit_atom]]


            dimensions=ts.dimensions
            usage.echo("%8.4f   %8.4f   %8.4f\r" %(dimensions[0],dimensions[1],dimensions[2]))

            for i in range(NUM_ATOMS):
               ts._x[i] =ts._x[i]+shift[0]
               if ts._x[i] > dimensions[0]:
                   ts._x[i]=ts._x[i]-dimensions[0]
               if ts._x[i] <0:
                   ts._x[i]=ts._x[i]+dimensions[0]

               ts._y[i] =ts._y[i]+shift[1]
               if ts._y[i] > dimensions[1]:
                   ts._y[i]=ts._y[i]-dimensions[1]
               if ts._y[i] <0:
                   ts._y[i]=ts._y[i]+dimensions[1]

               ts._z[i] =ts._z[i]+shift[2]
               if ts._z[i] > dimensions[2]:
                   ts._z[i]=ts._z[i]-dimensions[2]
               if ts._z[i] < 0:
                   ts._z[i]=ts._z[i]+dimensions[2]


#             temp_list=list()
#             for atom in atom_l:
#                 if atom.residue_serial in fitting_group:
#                     temp_list.append([\
#                             ts._x[atom_l.index(atom)],\
#                             ts._y[atom_l.index(atom)],\
#                             ts._z[atom_l.index(atom)],\
#                             ])


# #            [Rotate,shift]=least_squares_fitting.Fitting(temp_list,origin_list)


#             atom_matrix=numpy.array([[ts._x[i],ts._y[i],ts._z[i]]for i in range(NUM_ATOMS)])

# #            resu_matrix=numpy.matrix(atom_matrix) * numpy.matrix(Rotate).T 
# #            resu_matrix=numpy.array(resu_matrix)

# #            for i in range(NUM_ATOMS):
# #                atom_matrix[i,0]=resu_matrix[i,0]+shift[0]
# #                atom_matrix[i,1]=resu_matrix[i,1]+shift[1]
# #                atom_matrix[i,2]=resu_matrix[i,2]+shift[2]
 

#             for i in range(NUM_ATOMS):
#                 ts._x[i]=atom_matrix[i,0]
#                 ts._y[i]=atom_matrix[i,1]
#                 ts._z[i]=atom_matrix[i,2]
        
 
#        w.write(ts)
        NOW_TIME=Time.time()
        BIN_TIME=NOW_TIME-START_TIME
        usage.echo(" "*40+"Converted frame %d, time used: %8.2f s, time left: %8.2f s \r" \
                % (ts.frame,BIN_TIME,BIN_TIME*(float(TRAJ_FRAMES)/ts.frame-1) ))
#    for ts in u.trajectory:
        w.write(ts)
#        usage.echo("Writting frame %d\r"  %ts.frame)
    w.close_trajectory()
    print "Converted %r --> %r" % (intrj, outtrj)



if __name__=="__main__":
    if len(sys.argv)!=4:
        Usage()
        sys.exit()

    topol =sys.argv[1] #PRMpbc
    intrj =sys.argv[2] #TRJpbc_bz2
    outtrj = sys.argv[3]
    Move_2_center(topol,intrj,outtrj)    




