#!/usr/bin/env python
"""
Created 2011.12.17
Used for fiting the system by Z-axis and origin cooridinate.
"""

from MDPackage import Simple_atom
from MDPackage import Move_atom
from MDPackage import usage
import sys


def Usage():
    print "Usage: Trj_modify.py topfile top_result"
    print ""

def Print_ProgInfo():
    ''' 
    Print program information. the version, some notice and tips.
    '''
    print " " 
    print "  "*13,"-)","Rotate_2_Z","(-"
    print " " 
    print "  "*12,"-)"," Version: %s " %usage.version ,"(-" 
    print " " 


if __name__=="__main__":
    Print_ProgInfo()
    if len(sys.argv)!=3:
        Usage()
        sys.exit()


    topol =sys.argv[1] #PRMpbc
    resu_file=sys.argv[2]

    atom_l=Simple_atom.Get_Simple_atom_list(topol)
    fitting_group=Simple_atom.Get_residue(topol,True)
    origin_coor,z_axis=Move_atom.Init_parm(atom_l,fitting_group)
    print origin_coor, z_axis

    # loop through the trajectory and write a frame for every step
    Z_axis=(0,0,1)
    origin_coor=(0,0,0)
    b_atom=Move_atom.Move(atom_l, fitting_group, origin_coor,Z_axis  )
    Simple_atom.Save_file(resu_file,b_atom)


