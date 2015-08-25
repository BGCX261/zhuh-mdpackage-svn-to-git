#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Created on 2011-1-14\n
@author: zhuh
@version: 0.1.0
@change:\n
    - 2011-1-14.\n
        - finished the function B{Read_traj()}.\n
    - 2011-01-19.\n
        - Modified the function B{Read_traj()} ,  to make it run faster. 
    - 2011-02-21.\n
        - Created a function B{Traj_2_coor()}
    - 2011-02-23.\n
        - Optimizting the function B{Traj_2_coor()}
'''

import Simple_atom
import unit_atom
import MDAnalysis
import os
import usage

class Coor:
    '''
    A simple class defined the coordinate of a atom. Which is coor_x ,  coor_y , \
            coor_z.
    '''
    coor_x = 0.0
    coor_y = 0.0
    coor_z = 0.0

    def __init__(self , coor_x , coor_y , coor_z):
        self.coor_x = coor_x
        self.coor_y = coor_y
        self.coor_z = coor_z

def Read_traj(coor_file , traj_file , atom_list):
    '''
    Reading in the coor_file traj_file and atom_list.return the coor list.\n
    Using the MDAnalysis to read the coor_file and traj_file , so the coor_file \
            can be *.gro or *.pdb ,  and the traj_file can be *.trr and *.xtc.  \
            Make sure that the coor_file and traj_file have the same number of\
            atoms. 
    Note: the unit of the out put for the trajectory is A.
    '''

    u = MDAnalysis.Universe(coor_file , traj_file)
    for ts in u.trajectory:
        temp_list = []
        for x in atom_list:
            coor_temp = Coor(ts._x[x-1] , ts._y[x-1] , ts._z[x-1])
            temp_list.append(coor_temp)
        yield temp_list

def Traj_2_coor(in_coor_file,traj_file,out_coor_file,atom_list,skip):
    '''
    Reading a trajectory file. output the frames to files like out_coor_file_1.pdb \n
    atom_list : a list of atom serial.\n
    out_coor_file: a file name, in pdb or gro format. a list of file based on the name\
            will be created for output.\n
    skip: a int number like 1,2,3,10. 
    '''
    Alist=Simple_atom.Get_Simple_atom_list(in_coor_file)
    Blist=[]
    for atom in Alist:
        if atom.atom_serial in atom_list:
            Blist.append(atom)
    '''Get the result atom list in Simple_atom class.'''

    u=MDAnalysis.Universe(in_coor_file,traj_file)
    for ts in u.trajectory:
        if ts.frame % skip ==0 :

            a,b=os.path.splitext(out_coor_file)
            temp_out_file=a+"_%d" %(int(ts.frame)/skip) + b
            if os.path.isfile(temp_out_file):
                #print "backup %s to %s" %(temp_out_file,"#"+temp_out_file+"#")
                usage.echo("backup %s to %s\r" %(temp_out_file,"#"+temp_out_file+"#"))

                try:
                    os.rename(temp_out_file,"#"+temp_out_file+"#")
                except OSError,e: 
                    print e
                    print "the file %s will be overwrited!" %temp_out_file
                    pass

            fp=open(temp_out_file,'w+')
            if temp_out_file.endswith(".gro"):
                fp.write("%d\n" %len(Blist))
            else:
                pass

            for atom in Blist:
                temp_class=unit_atom.unit_atom(atom_name=atom.atom_name,\
                        atom_serial=atom.atom_serial,\
                        residue_name=atom.residue_name,\
                        residue_serial=atom.residue_serial)
                temp_class.atom_coor_x=ts._x[atom.atom_serial-1]/10
                temp_class.atom_coor_y=ts._y[atom.atom_serial-1]/10
                temp_class.atom_coor_z=ts._z[atom.atom_serial-1]/10

                if temp_out_file.endswith(".pdb"):
                    fp.write(temp_class.atom_2_PDBformat()+"\n")
                elif temp_out_file.endswith(".gro"):
                    fp.write(temp_class.atom_2_GROformat()+"\n")
                else:
                    pass

          #  print "write frame %5d to %16s" %(ts.frame,temp_out_file)
            usage.echo("write frame %5d to %16s\r" %(ts.frame,temp_out_file))

        else:
            pass

    return True


