#-*- coding:utf-8 -*-
'''
Created on 2011-1-10.
这个module主要目的是用于读取index.ndx文件，以及对之的处理。\n
@author: zhuh
@version: 0.1.0
@change: \n
    - 2011-1-10.\n
        - function B{Read_index_to_Inclass()} not finished.\n
    - 2011-1-11.\n
        - function B{Read_index_to_Inclass()} finished.\n
        - function B{Print_Index()} finished.\n
    - 2011-2-16.\n
        - Add function B{Atomlist_2_Index()} and it test OK.\n
    - 2011-3-16.\n
        - Update the Read_index_to_Inclass(). Fixed a problem.
    - 2012-08.07.\n
        - Finished the Write_Index() function. update the Index_class() class. 
'''

import re
import os

class Index_class:
    '''
    Core class
    '''
    group_name = " "
    group_list = []
    def __init__(self , group_name = " " , group_list = []):
        ''' Initialzation. '''
        self.group_name = group_name
        self.group_list = group_list
    def __str__(self):
        return "Group %15s has %6d elements" %(self.group_name , len(self.group_list))
    def __repr__(self):
        return "Group %15s has %6d elements" %(self.group_name , len(self.group_list))
        


def Read_index_to_Inclass(filename):
    '''Read in a index.ndx file ,  and return a list of Index_class'''
    try:
        fp = open(filename , 'r')
    except:
        sys.exc_info()[1]

#    line = fp.readline()
#    list = []
#    while len(line)>1:
#        temp_Index_class = Index_class()
#        if ("[" in line) :
#            temp_Index_class.group_name = (line.split(" "))[1]
#            temp_Index_class.group_list = []
#            line = fp.readline()
#            while( "[" not in line) and len(line)>1 :
#                line_units = re.split("\s+" , line.strip())
#                for s in range (len(line_units)):
#                    temp_Index_class.group_list.append(int(line_units[s]))
#                line = fp.readline()
#        list.append(temp_Index_class)
#    return list            

    list=[]
    temp_Index_class=Index_class()
    for line in fp:
        if ("[" in line):
       #     print line
            if  len(temp_Index_class.group_list)!=0:
              #  temp=Index_class()
                temp=temp_Index_class
                list.append(temp)
                temp_Index_class=Index_class()
            temp_Index_class.group_name=(line.split(" "))[1]
            temp_Index_class.group_list=[]
        elif len(line)>1: 
            line_units= re.split("\s+",line.strip())
            for s in line_units:
                temp_Index_class.group_list.append(int(s))
        else:
            pass
    list.append(temp_Index_class)
    fp.close()
    return list


def Print_Index(index_list):
    '''Print the index list like Gromacs does.'''
    for i in range(len(index_list)):
        print "Group %4d (%15s) has %6d elements" %(i , index_list[i].group_name , len(index_list[i].group_list))

def Atomlist_2_Index(atom_list):
    '''
    This function is used to Create a group list from a atom list which read from a structure file like gro or pdb.
    '''
    index_list=[]

    index_sys=Index_class()
    index_sys.group_name="System"
    for a in atom_list:
        index_sys.group_list.append(a.atom_serial)
    index_list.append(index_sys)

    for a in atom_list:
        if len(index_list)==0 :
            index_temp=Index_class()
            index_temp.group_name=a.residue_name
            index_temp.group_list.append(a.atom_serial)
            index_list.append(index_temp)
        else:
            name_list=[index_list[i].group_name for i in range(len(index_list))]
            if a.residue_name in name_list:
                index_list[name_list.index(a.residue_name)].group_list.append(a.atom_serial)
            else:
                index_temp=Index_class()
                index_temp.group_name=a.residue_name
                index_temp.group_list=[a.atom_serial]
                index_list.append(index_temp)

    return index_list

def Write_Index(index_list,filename):
    '''
    Writting a index type file from a Index class list.
    '''
    if os.path.isfile(filename):
        try:
            os.rename(filename,"#"+filename+"#")
            print "backup file %s to %s" %(filename,"#"+filename+"#")
        except OSError,e:
            print e
    try:
        fp=open(filename,'w+')
    except:
        print "except in opening %s" %filename
        return False

    for index in index_list:
        fp.write("[ "+index.group_name+" ]\n")
        COUNT=0
        for ind in index.group_list:
            COUNT=COUNT+1
            temp_str=str(ind)
            if len(temp_str)<5:
                fp.write("%4s " %temp_str)
            else:
                fp.write("%s " %temp_str)
            if COUNT % 15 ==0:
                fp.write("\n")
        fp.write("\n")
    print "Write the index file: %s" %filename


    
