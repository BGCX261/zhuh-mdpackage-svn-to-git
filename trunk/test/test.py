#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Create on 2011-01-15.
用来测试各函数。
@change:\n
    - 2011.01.15
        - test the function B{Get_ratate_matrix()}
    - 2011.01.24
        - Add test_da.py to this file.

'''
import numpy
from MDPackage import parallel_analysis
from MDPackage import twist_in_GDNA
from MDPackage import GRO
from MDPackage import PDB
from MDPackage import PQR
from MDPackage import Index
from MDPackage import Traj
from MDPackage import amber_top
from MDPackage.data_analysis import Average
import unittest
from MDPackage import Move_atom
from MDPackage import Simple_atom

gro_file="confout.gro"
pdb_file="confout.pdb"
traj_file="trajout.xtc"
pqr_file="MOL.pqr"
idx_file="index.ndx"
amb_file="2GKU.top"


def test_Get_rotate_matrix():
    exper_coor=numpy.array([
        [ 11.417, -2.904, -4.880],
        [ 10.759, -1.995, -5.662],
        [ 11.469, -0.913, -5.867],
        [ 12.638, -1.108, -5.156],
        [ 13.759, -0.273, -5.036],
        [ 14.767, -0.848, -4.249],
        [ 14.663, -2.116, -3.719],
        [ 13.625, -2.934, -3.830],
        [ 12.625, -2.328, -4.545]
        ])
    base_name='G'
    A,B=parallel_analysis.Get_rotate_matrix(exper_coor,base_name)
    print A
    print B

def test_Get_RMSD():
    exper_coor=numpy.array([
        [ 11.417, -2.904, -4.880],
        [ 10.759, -1.995, -5.662],
        [ 11.469, -0.913, -5.867],
        [ 12.638, -1.108, -5.156],
        [ 13.759, -0.273, -5.036],
        [ 14.767, -0.848, -4.249],
        [ 14.663, -2.116, -3.719],
        [ 13.625, -2.934, -3.830],
        [ 12.625, -2.328, -4.545]
        ])
    base_name='G'
    rotation=numpy.array([
        [-0.2331, -0.8862, -0.4004],
        [ 0.8249, -0.3983,  0.4012],
        [-0.5150, -0.2368,  0.8238]
        ])
    origin=numpy.array([15.1632 , -0.0362 , -4.4678])
    A=parallel_analysis.Get_RMSD(exper_coor,base_name,origin,rotation)
    print A


def test_Rotate_2_vector():
    vector1=[-0.3781,0.5388,0.7528]
    vector2=[-0.4326,0.6579,0.6165]
    resu=parallel_analysis.Rotate_2_vector(vector1,vector2)
    print resu

def test_Get_parallel_result():
#    list1=[2]
#    list2=[3,9,17,21]
    list1=[1]
    list2=[2,5]
#    traj_file="/home/zhuh/Mount/99/ExPag/G4_ligand/2GKU-NMR/traj.xtc"
#    coor_file="/home/zhuh/Mount/99/ExPag/G4_ligand/2GKU-NMR/origin.pdb"
    global traj_file
    global gro_file
    parallel_analysis.Get_parallel_result(traj_file,gro_file,list1,list2,"parallel.xvg")

def test_Get_twist_in_GDNA():
    list1=[1,6,10,15]
    list2=[2,5,11,14]
    global traj_file
    global pdb_file
    twist_in_GDNA.Get_twist_in_GDNA(traj_file,pdb_file,list1,list2,"twist.xvg")

def test_Read_data_4_average():
    file_name="parallel.xvg"
    row=2
    resu=Average.Read_data_4_averge(file_name,row)
    print resu

def test_GRO_Get_atom_List():
    global gro_file
    atom_list=GRO.Get_Atom_list(gro_file)
#    for i in range(20):
#        print atom_list[i].atom_2_GROformat()
    for i in range(20):
        print atom_list[i].atom_2_PDBformat()

def test_PDB_Get_atom_List():
    global pdb_file
    atom_list=PDB.Get_Atom_list(pdb_file)
    for i in range(20):
        print atom_list[i].atom_2_PDBformat()
#    for i in range(20):
#        print atom_list[i].atom_2_GROformat()



def test_Index_Read_index_to_Inclass():
    global idx_file
    in_list=Index.Read_index_to_Inclass(idx_file)
    Index.Print_Index(in_list)


def test_Index_Atomlist_2_Index():
    global gro_file
    atom_list=GRO.Get_Atom_list(gro_file)
    index_list=Index.Atomlist_2_Index(atom_list)
    Index.Print_Index(index_list)

def test_Traj_2_coor():
    global gro_file
    global traj_file
    atom_list=[1,2,3,4,5,6,7,8,9]
    Traj.Traj_2_coor(gro_file,traj_file,"test.gro",atom_list,2)

def test_PQR_Get_Atom_list():
    global pqr_file
    atom_list=PQR.Get_Atom_list(pqr_file)
    for i in range(5):
        print atom_list[i].atom_2_PQRformat()

def test_amber_top():
    aa=amber_top.Read_top("2GKU.top")
    print "hello world."

def test_move_atom():
    a_atom=Simple_atom.Get_Simple_atom_list("2GKU.pdb")
    b_atom=Simple_atom.Get_Simple_atom_list("2GKU_md1.pdb")
    origin_coor_old,z_axis_old=Move_atom.Init_parm(a_atom,[1])
    print origin_coor_old
    print z_axis_old
    c_atom=Move_atom.Move(b_atom,[1],origin_coor_old,z_axis_old)
    origin_coor,z_axis=Move_atom.Init_parm(c_atom,[1])
    print origin_coor
    print z_axis
    for i in range(20):
        print a_atom[i].atom_2_PDBformat()
        print c_atom[i].atom_2_PDBformat()




if __name__=="__main__":
#    test_Get_rotate_matrix()
#    test_Rotate_2_vector()
#    test_Get_parallel_result()
#    test_Get_RMSD()   
#    test_Get_twist_in_GDNA()
#    test_GRO_Get_atom_List()
#    test_PDB_Get_atom_List()
#    test_Read_data_4_average()
#    test_Index_Atomlist_2_Index()
#    test_Traj_2_coor()
#    test_PQR_Get_Atom_list()
#    test_Index_Read_index_to_Inclass()
#    test_amber_top()
    test_move_atom()

