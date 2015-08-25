#!/usr/bin/env python
"""
A script used for split the les trajectory.
"""

#from MDAnalysis.tests.datafiles import PRMpbc,TRJpbc_bz2
#from MDAnalysis.tests.datafiles import PRM,TRJ_bz2
from MDAnalysis import Universe, Writer
from MDAnalysis.core.util import greedy_splitext
from MDAnalysis.coordinates.base import Timestep

from G4Analysis import Simple_atom
from G4Analysis import usage
import os.path
import sys
import copy


def Usage():
    print "Usage: LES_2_dcd.py topfile trjfile"

def Check(atom_list):
    NUM=1
    FIND=False
    FINISHED=False
    new_list=list()
    store_list=list()
    START=0
    END=0
    new_list.append(atom_list[0])
    for atom in atom_list[1:]:
        if atom.atom_name != new_list[-1].atom_name or atom.residue_serial!=new_list[-1].residue_serial:
            new_list.append(atom)


            FIND=False
            if NUM!=1:
                FIND=True
            if FIND:
                if END> 1 and END < len(new_list)-1:
                    FINISHED=True

        elif not FIND:
            NUM=NUM+1
            START=len(new_list)

        elif FIND and not FINISHED:
            END=len(new_list)

        if FINISHED:
            print START,END,NUM
            store_list.append([START,END,NUM])
            FINISHED=False
            FIND=False
            NUM=1
            END=1

    return new_list,store_list

def Run(topol,intrj):
    ext='.dcd'
    atom_l=Simple_atom.Get_Simple_atom_list(topol)
    new_list,store_list=Check(atom_l)

    NUM=store_list[0][2]
    for a in store_list:
        if NUM> a[2]:
            NUM=a[2]
        

    root, oldext = greedy_splitext(os.path.basename(intrj))
    outpdb = root + '.pdb'

    u = Universe(topol, intrj)
    NUM_ATOMS=len(new_list)

    # create a writer instance for the output trajectory
    outtrj = [root+str(i)+ ext for i in range(NUM)]
    w =[ Writer(outtrj[i], NUM_ATOMS) for i in range(NUM)]
    Atom_list=[copy.deepcopy(new_list) for i in range(NUM)]
    '''
    NUM copies new_list   
    '''

    # loop through the trajectory and write a frame for every step
    for ts in u.trajectory:
        for i in range(NUM_ATOMS):
            if i < store_list[0][0]-1 :
                for s in range(NUM):
                    Atom_list[s][i].atom_coor_x=ts._x[i]
                    Atom_list[s][i].atom_coor_y=ts._y[i]
                    Atom_list[s][i].atom_coor_z=ts._z[i]

            elif i > store_list[-1][1]-1:
                LENGTH=0
                for a in store_list:
                    LENGTH=LENGTH+(a[2]-1)*(a[1]-a[0]+1)
                for s in range(NUM):
                    Atom_list[s][i].atom_coor_x=ts._x[i+LENGTH]
                    Atom_list[s][i].atom_coor_y=ts._y[i+LENGTH]
                    Atom_list[s][i].atom_coor_z=ts._z[i+LENGTH]
            else:
                LENGTH=0
                for j in range(len(store_list)):
                    if i > store_list[j][0]-2 and i < store_list[j][1]:
                        if j > 0:
                            for a in store_list[:j]:
                                LENGTH=LENGTH+(a[2]-1)*(a[1]-a[0]+1)
                        else:
                            LENGTH=0

                        for s in range(NUM):
                            Atom_list[s][i].atom_coor_x=ts._x[store_list[j][0]-1+LENGTH+s+(i+1-store_list[j][0])*store_list[j][2]]
                            Atom_list[s][i].atom_coor_y=ts._y[store_list[j][0]-1+LENGTH+s+(i+1-store_list[j][0])*store_list[j][2]]
                            Atom_list[s][i].atom_coor_z=ts._z[store_list[j][0]-1+LENGTH+s+(i+1-store_list[j][0])*store_list[j][2]]

                for j in range(len(store_list)-1):
                    if i > store_list[j][1]-1 and i < store_list[j+1][0]-1:
                        for a in store_list[:j+1]:
                            LENGTH=LENGTH+(a[2]-1)*(a[1]-a[0]+1)

                        for s in range(NUM):
                            Atom_list[s][i].atom_coor_x=ts._x[i+LENGTH]
                            Atom_list[s][i].atom_coor_y=ts._y[i+LENGTH]
                            Atom_list[s][i].atom_coor_z=ts._z[i+LENGTH]

        
        new_ts=[Timestep(NUM_ATOMS) for i in range(NUM)]
        

        for i in range(NUM_ATOMS):
            for s in range(NUM):
                new_ts[s]._x[i]=Atom_list[s][i].atom_coor_x
                new_ts[s]._y[i]=Atom_list[s][i].atom_coor_y
                new_ts[s]._z[i]=Atom_list[s][i].atom_coor_z

        for s in range(NUM):
            w[s].write(new_ts[s])
        usage.echo("Converted frame %d\r" % ts.frame)
    for s in range(NUM):
        w[s].close_trajectory()
    print "Converted %r --> %r" % (intrj, outtrj)

    # make a pdb file as a simple 'topology'
    u.trajectory.rewind()
    for atom in Atom_list[0]:
        atom.atom_coor_x=atom.atom_coor_x/10
        atom.atom_coor_y=atom.atom_coor_y/10
        atom.atom_coor_z=atom.atom_coor_z/10

    Simple_atom.Save_file(outpdb,Atom_list[0])
    print "Created %r to be used with the trajectory" % outpdb


if __name__=="__main__":
    if len(sys.argv)!=3:
        Usage()
        sys.exit()

    topol =sys.argv[1] #PRMpbc
    intrj =sys.argv[2] #TRJpbc_bz2

    Run(topol,intrj)


