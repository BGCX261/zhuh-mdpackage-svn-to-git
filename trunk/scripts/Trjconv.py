#!/usr/bin/env python

'''
Created on 2011-02-22.
It's used for convert a trajectory file to a list of structure file.
@change:
    - 2011-02-22.\n
        - Finished it, but many code are instead by B{pass}.
    - 2011-03-13.\n
        - Modified the usage
'''

from MDPackage import Traj
from MDPackage import Index
from MDPackage import Simple_atom
from MDPackage import usage
import sys
import getopt
import os

def Cheak_args():

    try:
        opts,argvs=getopt.getopt(sys.argv[1:],"hp:f:n:o:",["skip="])
    except getopt.GetoptError,e:
        print e
        Usage()
        sys.exit()

    traj_file=""
    coor_file=""
    out_coor_file="confout.gro"
    index_file=""
    skip=1
    for a,b in opts:
        if a == "-f":
            traj_file=b
        elif a == "-n":
            index_file=b
        elif a == "-p":
            coor_file=b
        elif a == "-o":
            out_coor_file=b
        elif a == "--skip":
            try:
                skip=int(b)
            except:
                pass
        elif a == "-h":
            Usage()
            sys.exit(0)
        else:
            pass
    if not os.path.isfile(traj_file):
        print "the trajectory file %s is not exist." %traj_file
        sys.exit(0)

    if not os.path.isfile(coor_file):
        print "the structure file %s is not exist." %coor_file
        sys.exit(0)

    if out_coor_file[-4:] not in [".pdb",".gro"]:
        print "error: the output structure must *.pdb or *.gro."
        sys.exit(0)
    
    if not os.path.isfile(index_file):
        atom_list=Simple_atom.Get_Simple_atom_list(coor_file)
        index_list=Index.Atomlist_2_Index(atom_list)
    else:
        index_list=Index.Read_index_to_Inclass(index_file)

    Index.Print_Index(index_list)
    group_ID=raw_input("Choose a group: ")
    try:
        atom_list=index_list[int(group_ID)].group_list
    except:
        print "error"
        sys.exit()
    Traj.Traj_2_coor(coor_file, traj_file, out_coor_file, atom_list, skip)

def Usage():
    print "Usage: Trjconv -p <coor_file> -f <traj_file> -n <index_file> -o <coor_file> --skip num"
    print ""
    usage.File_input()
    usage.Print_line()
    usage.Coor_file("coor_file","Input")
    usage.Traj_file("traj_file","Input")
    usage.Ind_file("index_file","Input")
    usage.Coor_file("coor_file","Output","-o")
    usage.Print_line()
    print ""
    usage.Type_input()
    usage.Print_line()
    usage.Show_skip(1)
    usage.Show_help("no")
    print ""



if __name__ == "__main__":
    print ""
    print "  "*12,"-)","  Trjconv.py  ","(-"
    print ""
    print "  "*12,"-)","Version: %s" %usage.version,"(-"
    print ""
    Cheak_args()
