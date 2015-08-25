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
from MDPackage.data_analysis import Average
import unittest

gro_file="confout.gro"
pdb_file="confout.pdb"
traj_file="trajout.xtc"
pqr_file="MOL.pqr"
idx_file="index.ndx"


class test_Get_rotate_matrix(unittest.TestCase):
    def test(self):
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
        result_A=numpy.array([
            [-0.2330924 , -0.88617613, -0.4004495 ],
            [ 0.82490543, -0.39825248,  0.40115583],
            [-0.51497473, -0.23682659,  0.82384112]
            ])
        result_B=numpy.array([ 15.16322121  -0.03615313  -4.46779855])
        self.assertEquals(A.any(),result_A.any())
        self.assertEquals(B.any(),result_B.any())

class test_Get_RMSD(unittest.TestCase):
    def test(self):
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
        result_A=0.0236
        self.assertTrue(abs(A-result_A)<0.0001)


class test_Rotate_2_vector(unittest.TestCase):
    def test(self):
        vector1=[-0.3781,0.5388,0.7528]
        vector2=[-0.4326,0.6579,0.6165]
        A=parallel_analysis.Rotate_2_vector(vector1,vector2)
        result_A=numpy.array([-0.4071778,   0.60105313,  0.68770734])
        self.assertTrue(abs(A.any()-result_A.any())<0.00001)

def test_Get_parallel_result():
    list1=[1]
    list2=[2,5]
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
    for i in range(20):
        print atom_list[i].atom_2_PDBformat()

def test_PDB_Get_atom_List():
    global pdb_file
    atom_list=PDB.Get_Atom_list(pdb_file)
    for i in range(20):
        print atom_list[i].atom_2_PDBformat()

def test_GRO_Get_Segment_list():
    global gro_file
    segment_list=GRO.Get_Segment_list(gro_file)
    print segment_list[:20]

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


def test_suite():
    def suite(test_class):
        return unittest.makeSuite(test_class)
    su=unittest.TestSuite()
    su.addTests((suite(test_Get_rotate_matrix),suite(test_Get_RMSD),suite(test_Rotate_2_vector)))
    return su


if __name__=="__main__":
#    test_Rotate_2_vector()
#    test_Get_parallel_result()
#    test_Get_RMSD()   
#    test_Get_twist_in_GDNA()
#    test_GRO_Get_atom_List()
#    test_PDB_Get_atom_List()
#    test_Read_data_4_average()
#    test_GRO_Get_Segment_list()
#    test_Index_Atomlist_2_Index()
#    test_Traj_2_coor()
#    test_PQR_Get_Atom_list()
#    test_Index_Read_index_to_Inclass()
    unittest.main(defaultTest='test_suite')
