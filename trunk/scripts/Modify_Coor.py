#!/usr/bin/env python

'''
Created 2011-02-16.
Created for convert a structure file form one format to another. Or load in a structure file, and 
modified it.
@change: \n
    - 2011-02-25.\n
        - Now it's run.
    - 2011-03-12.\n
        - Modified the Usage.\n
'''

#from MDPackage import PDB
#from MDPackage import GRO
from MDPackage import PQR
from MDPackage import Simple_atom
from MDPackage.Simple_atom import Save_file
from MDPackage import Index
from MDPackage import usage
import re
import string
import sys
import os
from termcolor import colored
import getopt

class Coord():
    def __init__(self):
        self.atom_list=list()
        self.group_list=list()
    def Load_file(self,filename,crd_file=""):
        '''
        It's used for loading in a structure file like pdb and gro.
        '''
        if os.path.isfile(filename):
            print "loading file %s..." %filename
        else:
            print "%s not exist!" %colored(filename,'red',attrs=['bold'])
        self.atom_list=Simple_atom.Get_Simple_atom_list(filename,crd_file)
        if len(self.atom_list)!=0:
            self.group_list=Index.Atomlist_2_Index(self.atom_list)

    def Delete_group(self,del_group_id):
        '''
        Delete a group from the group_list and atom_list.
        '''
        if del_group_id in range(len(self.group_list)):
            delete_list=self.group_list[del_group_id].group_list
            atom_serial_list=[self.atom_list[i].atom_serial for i in range(len(self.atom_list))]
            for i in delete_list:
                usage.echo("remove atom %8d, atom name %6s\r" %(i,self.atom_list[atom_serial_list.index(i)].atom_name))
                self.atom_list.remove(self.atom_list[atom_serial_list.index(i)])
                '''remove a atom form atom list'''
                self.group_list[0].group_list.remove(self.group_list[0].group_list[atom_serial_list.index(i)])
                '''remove a atom from group_list[0] which is named system'''
                atom_serial_list.remove(i)
            print "deleted group %s, %6d atoms" %(self.group_list[del_group_id].group_name,len(delete_list))

            self.group_list.remove(self.group_list[del_group_id])
        else:
            print "you input a number not in the list. %d" %del_group_id

    def Save(self,file_name):
        self.atom_list=Simple_atom.Check_list(self.atom_list)
        try:
            result=Save_file(file_name,self.atom_list)
        except:
            print "Some problem happened when write file."


def Main_Loop( ):
    '''
    The main loop, for input and output, like load file ,save file, list groups, delete groups etc.
    '''
    history=[]
    main_list=list()
    while True:

        line=raw_input(" > ")
        history.append(line)

        if len(line)==0:
            if len(main_list)>0:
                Index.Print_Index(main_list[0].group_list)
                print ""
            else:
                print "No molecule load.\n"
                continue
            
        temp=re.split("\s+",string.strip(line)) 

        if string.lower(temp[0]) == "quit":
            break

        elif string.lower(temp[0]) == "help":
            Help(line)

        elif string.lower(temp[0]) == "history":
            Print_History(history)

        elif string.lower(temp[0]) == "load":
            coor=Coord()
            if len(temp) == 2 and temp[1] != "":
                coor.Load_file(temp[1])
                Index.Print_Index(coor.group_list)
                main_list.append(coor)
                print ""
            elif len(temp) == 3 and temp[2] != "":
                coor.Load_file(temp[1],temp[2])
                Index.Print_Index(coor.group_list)
                main_list.append(coor)
                print ""
            else:
                print "Usage: load <filename>  : Load a structure like gro, pdb."

        elif string.lower(temp[0]) == "list":
            if len(main_list)>0:
                Index.Print_Index(main_list[0].group_list)
                print ""
            else:
                print "No molecule load.\n"

        elif string.lower(temp[0]) == "delete":
            if len(temp) == 2 and temp[1] != "":
                try:
                    del_id=int(temp[1])
                except:
                    pass
                if del_id>0:
                    main_list[0].Delete_group(del_id)
                elif del_id==0:
                    main_list[0]=list()
            else:
                pass

        elif string.lower(temp[0]) == "save":
            main_list[0].Save(temp[1])

        else:
            os.system(line)
        #    print "command " + colored(line,'red',attrs=['bold']) + " is invalid." 
        #    print "type %s to see more information." %colored("help",'red',attrs=['bold'])



def Help(line):
    '''
    print help information.
    '''
    if line == "help":
        Loop_Usage()
    else:
        pass

def Loop_Usage():
    '''
    print the simplify usage information. 
    '''
    print ""
    print "%s      <filename>  : Load a structure file: gro pdb etc." %colored("load",'red',attrs=['bold'])
    print "%s                  : List the groups."%colored("list",'red',attrs=['bold'])
    print "%s               : List the groups."%colored("<Enter>",'red',attrs=['bold'])
    print " "
    print "delete    <groupname> : Delete a group."
    print "splitres  <groupname> : Split a group to residues."
    print "splitatom <groupname> : Split a group to atoms."
    print ""
    print "save      <filename>  : Save the result to a structure file: gro pdb etc."
    print ""
    print "history               : Print the input history."
    print "help                  : Print help information."
    print "quit                  : Quit."
    print ""

def Main_Usage():
    '''
    '''
    print "Modify_Coor convert a structure file from one format to another or modified the structure file."
    print "The structure file can be in pdb, gro or pqr."
    print ""
    print "Usage:"
    print colored("Modified.py",'red',attrs=['bold'])+" to run interactive mode."
    print colored("Modified.py -f <filename> -o <filename>",'red',attrs=['bold'])+" to run command mode."
    print ""


def Print_History(history):
    '''
    print the input history.
    '''
    for i in range(len(history)):
        if len(history[i])>0:
            print "%4d  %s" %(i+1,colored(history[i],'red',attrs=['bold']))
        else:
            print "%4d  %s" %(i+1,colored("<Enter>",'red',attrs=['bold']))

def Cheak_argv():
    '''
    cheak the input argv.
    '''
    if len(sys.argv) == 1 :
        Main_Loop()
    elif len(sys.argv) ==2:
        if sys.argv[1] == "-h":
            Main_Usage()
        else:
            pass
    elif len(sys.argv) == 5:
        in_file=""
        out_file=""
        opts,args=getopt.getopt(sys.argv[1:],"hf:o:")
        for a,b in opts :
            if a == "-f":
                in_file=b
            elif a=="-o":
                out_file=b
            else:
                pass

        coor=Coord()
        coor.Load_file(in_file)
        coor.Save(out_file)

    else:
        pass

if __name__ == "__main__":
    print ""
    print "  "*12,"-)","   Modify_Coor  ","(-"
    print ""
    print "  "*12,"-)"," Version: %s " %usage.version ,"(-"
    print ""
    Cheak_argv()
