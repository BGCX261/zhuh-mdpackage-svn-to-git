# -*- coding : utf-8 -*-

from G4Analysis import Simple_atom
from G4Analysis import DNA_matrix
from numpy import dot
import numpy
import math

   
def Move(atom_list, fitting_group, origin_coor, z_axis ):
    origin_coor_old,z_axis_old=Init_parm(atom_list,fitting_group)
#    print z_axis_old

    ga=math.acos(dot(z_axis,z_axis_old))
#    print ga
    cross_vector = numpy.cross(z_axis, z_axis_old)
    cv = cross_vector/math.sqrt(numpy.dot(cross_vector, cross_vector))
#    print cv

    for atom in atom_list:
        ve=[atom.atom_coor_x,atom.atom_coor_y,atom.atom_coor_z]
        R=DNA_matrix.Rotate_matrix(-ga,cv)
        resu=numpy.matrix(R)*(numpy.matrix(ve).T)
#        print resu[0],resu[1],resu[2]
#        print float(resu[0]),float(resu[1]),float(resu[2])
        atom.atom_coor_x=float(resu[0])
#        print atom.atom_coor_x
        
        atom.atom_coor_y=float(resu[1])
        atom.atom_coor_z=float(resu[2])

    origin_coor_old,z_axis_old=Init_parm(atom_list,fitting_group)
    move_coor=[origin_coor[i]-origin_coor_old[i] for i in range(3)]
    for atom in atom_list:
        atom.atom_coor_x=atom.atom_coor_x+move_coor[0]
        atom.atom_coor_y=atom.atom_coor_y+move_coor[1]
        atom.atom_coor_z=atom.atom_coor_z+move_coor[2]

    pass


    return atom_list


def Init_parm(atom_list, fitting_group):
    residue_list=Simple_atom.Get_Residue_list(atom_list)
    base_name_list=list()
    base_atom_list=list()

    base_name_list= [residue_list[j-1][0] for j in fitting_group]
    base_atom_list= [DNA_matrix.Get_baseID_list(atom_list,j) for j in fitting_group]

    r1=[]
    '''the group 1 rotate list'''
    c1=[]
    '''the group 1 coordinate list'''
    for m in range(len(fitting_group)):
        temp_list = [ [atom_list[x-1].atom_coor_x, atom_list[x-1].atom_coor_y, atom_list[x-1].atom_coor_z] for x in base_atom_list[m] ]
        result = DNA_matrix.Get_rotate_matrix(numpy.array(temp_list), base_name_list[m])
        c1.append(numpy.array(temp_list))
        r1.append(result)
 
    z_axis,origin_coor = DNA_matrix.Get_group_rotmat(r1,len(base_name_list))
    return origin_coor,z_axis

