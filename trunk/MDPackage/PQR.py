'''
Created on 2011-02-28.
@change: \n
    - 2011-02-28.\n
        - Created.
'''


import Simple_atom
import os
import sys
import re
import string

class PQR():
    '''
    PQR class. It's similar to PDB class.
    '''
    atom_name=""
    atom_serial=0
    residue_name=""
    residue_serial=0
    atom_coor_x=0.0
    atom_coor_y=0.0
    atom_coor_z=0.0
    atom_charge=0.0
    atom_radius=0.0
    def __init__(self,atom_name="",atom_serial=0,residue_name="",residue_serial=0,\
            atom_coor_x=0.0,atom_coor_y=0.0,atom_coor_z=0.0,atom_charge=0.0,\
            atom_radius=0.0):
        self.atom_name=atom_name
        self.atom_serial=atom_serial
        self.atom_coor_x=atom_coor_x
        self.atom_coor_y=atom_coor_y
        self.atom_coor_z=atom_coor_z
        self.atom_charge=atom_charge
        self.atom_radius=atom_radius
        self.residue_name=residue_name
        self.residue_serial=residue_serial

    def atom_2_PQRformat(self):
        '''
         convert a PQR class to a pqr format string.
        '''
        temp_atom=""
        if re.match('^\d',self.atom_name) != None:
            temp_atom=self.atom_name.ljust(4)
        else:
            if len(self.atom_name)<4:
                temp_atom=(" "+self.atom_name).ljust(4)
            else:
                temp_atom=self.atom_name
        s = "%s%5d %s %3s  %4d    %8.3f%8.3f%8.3f%8.4f%7.4f "  \
                % ("ATOM".ljust(6) , self.atom_serial , temp_atom , self.residue_name.rjust(3),\
                self.residue_serial , self.atom_coor_x*10 , self.atom_coor_y*10 , self.atom_coor_z*10,\
                self.atom_charge,self.atom_radius)
        return s

def Get_Atom_list(filename):
    '''
    Read in a pqr file and return a pqr atom list.
    '''
    if os.path.isfile(filename):
        fp=open(filename,'r')
    else:
        print "Error: No such file: %s" %filename 
        sys.exit(0)

    lines=fp.readlines()
    atom_list=[]
    for eachline in lines:
        if (eachline.startswith("ATOM")) or (eachline.startswith("HETEAM")):

            temp_Atom_class = PQR()
            try:
                temp_Atom_class.atom_serial = int(string.strip(eachline[6:11]))
            except:
                pass
            temp_Atom_class.atom_name = string.strip(eachline[12:16])
            temp_Atom_class.residue_name = string.strip(eachline[17:20])
            try:
                temp_Atom_class.residue_serial = int(string.strip(eachline[22:26]))
            except:
                pass
            try:
                temp_Atom_class.atom_coor_x = float(string.strip(eachline[30:38]))/10
                temp_Atom_class.atom_coor_y = float(string.strip(eachline[38:46]))/10
                temp_Atom_class.atom_coor_z = float(string.strip(eachline[46:54]))/10
            except:
                pass
            try:
                temp_Atom_class.atom_charge = float(eachline.split()[-2])
                temp_Atom_class.atom_radius = float(eachline.split()[-1])
            except:
                print "error"
        
            atom_list.append(temp_Atom_class)
        else:
            pass
    return atom_list

