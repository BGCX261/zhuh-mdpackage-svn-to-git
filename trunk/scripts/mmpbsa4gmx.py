#! /usr/bin/env python
'''
'''
import string
import sys
import os
import re
import math
from subprocess import Popen, PIPE, STDOUT
#from MDPackage import usage
    
K= 1.3806504e-23
'''It's the Boltzmann constant'''
HBA= 1.05457148e-34
'''It's the Planck constant'''
R= 8.3145
'''It's the idea gas constant'''
E= 2.71828183
'''natural exp poment e'''
CYCLE=20
'''the number of the bins'''
    
def Checkargs():
    argc=len(sys.argv)
    if argc != 3:
        Usage()
        exit()
    my_hash=Read_input(sys.argv[2])
    Calculate_entropy(my_hash)
        
def Usage():
    '''Print the usage information'''
    print    "Usage : entropy2gmx.py [option] <input file>"
    print    "options:"
    print    "\t -h\t bool\t\t no\t Print help infomation and quit."
    print    "\t -v\t bool\t\t no\t Be loud and noisy."
    print    "\t -i\t input.in\t Input\t Set input file."

def Read_input(filename):
    '''Read the input.in file and return a hash which include all the information.
    It's also check if the information is right.'''
    my_hash={}
    try:
        fh=open(filename,'r')
    except:
        print filename,":",sys.exc_info()[1]
        
    allLines=fh.readlines()
    fh.close()
       
    for eachline in allLines:
        
        m=re.match('^#',eachline)
        n=re.match('\s+',eachline)
        if m ==None and n==None:
            line_units=re.split('\s+',eachline)
            if line_units[0] == "traj_name":
                if os.path.isfile(line_units[1]):
                    my_hash["traj_name"]=line_units[1]
                else:
                    print "Error:the traj file not exist!"
                    exit(1)
            elif line_units[0] == "index_name":
                my_hash["index_name"]=line_units[1]
            elif line_units[0] == "begin_time":
                my_hash["begin_time"]=line_units[1]
            elif line_units[0] == "end_time":
                my_hash["end_time"]=line_units[1]    
            elif line_units[0] == "Out_file":
                my_hash["Out_file"]=line_units[1]
            elif line_units[0] == "Temp":
                my_hash["Temp"]=line_units[1]
            elif line_units[0] == "Algorithm":
                my_hash["Algorithm"]=line_units[1]
            elif line_units[0] == "tpr_name":
                if os.path.isfile(line_units[1]):
                    my_hash["tpr_name"]=line_units[1]
                else:
                    print "Error:the tpr file not exist!"
                    exit(2)
            elif line_units[0] == "group_name":
                for count in range(len(line_units)):
                    if string.find(line_units[count],'#')>-1:
                        my_hash["group_name"]=string.join(line_units[1:count], ':')
                        break
            else:
                print "paramter",line_units[0],"was not defined"
    
    if (len(my_hash)!=9):
        if (my_hash.has_key('traj_name')==0):
            print "need parameter traj_name"
        if (my_hash.has_key('index_name')==0):
            print "need parameter index_name"
        if (my_hash.has_key('begin_time')==0):
            print "need parameter begin_time"
        if (my_hash.has_key('end_time')==0):
            print "need parameter end_time"    
        if (my_hash.has_key('Out_file')==0):
            print "need parameter Out_file"
        if (my_hash.has_key('Temp')==0):
            print "need parameter Temp"
        if (my_hash.has_key('Algorithm')==0):
            print "need parameter Algorithm"
        if (my_hash.has_key('tpr_name')==0):
            print "need parameter tpr_name"
        if (my_hash.has_key('group_name')==0):
            print "need parameter group_name"
        exit()
    else:
        print "Finish reading all parameters."
        
    return my_hash

def Read_index(index_file_name):
    '''It's read the index file to return a hash group_name->group_index.'''
    try:
        fh=open(index_file_name,'r')
    except:
        print index_file_name,":",sys.exc_info()[1]
    
    AllLines=fh.readlines()
    fh.close()
    num=0
    hash_in={}
    for eachline in AllLines:
        if string.find(eachline,'[')>-1:
            hash_in[re.split('\s+',eachline)[1]]=num
            num+=1
    
    print "Finish reading index file",index_file_name
    return hash_in
               
    
def Run_commd(commd,group_index,circle_index):
    '''Just used to run commd by Popen.'''
    pf=Popen(commd,stdin=PIPE,stdout=PIPE,stderr=STDOUT,shell=True)  
    pf.stdin.write("%d\n"%group_index)
    pf.stdin.write("%d\n"%group_index)


    print "It's the circle %s" %circle_index
    print "Waiting for calculating the eigenvalue and eigenvector files......"
    pf.wait()

#    print pf.stdout.read()
    print "It's finished! "
  
def Write_mdp(filename):
    fp=open(filename,"w+")
    fp.write("define = -DFLEXIBLE\n")
    fp.write("integrator               = md\n")
    fp.write("nsteps                   = 0\n")
    fp.write("dt                       = 0.001\n")
    fp.write("constraints              = none\n")
    fp.write("emtol                    = 10.0\n")
    fp.write("emstep                   = 0.01\n")
    fp.write("nstcomm                  = 1\n")
    fp.write("ns_type                  = simple\n")
    fp.write("nstlist                  = 0\n")
    fp.write("rlist                    = 0\n")
    fp.write("rcoulomb                 = 0\n")
    fp.write("rvdw                     = 0\n")
    fp.write("Tcoupl                   = no\n")
    fp.write("Pcoupl                   = no\n")
    fp.write("gen_vel                  = no\n")
    fp.write("nstxout                  = 1\n")
    fp.write("pbc                      = no\n")
    fp.write("nstlog = 1\n")
    fp.write("nstenergy = 1\n")
    fp.write("nstvout = 1\n")
    fp.write("nstfout = 1\n")
    fp.write("nstxtcout = 1\n")
    fp.write("comm_mode = ANGULAR\n")
    fp.write("continuation = yes\n")
    fp.close()

def Write_apbs(filename,pqrname,temp=300,TYPE="SP"):
    fp=open(filename,"w+")
    fp.write("read\n")
    fp.write("mol pqr %s\n" %(pqrname))
    fp.write("end\n")

    if TYPE=="SP":
        fp.write("elec name 1_solv\n") # Electrostatics calculation on the solvated state
        fp.write("       mg-manual \n")# Specify the mode for APBS to run
        fp.write("       dime 129 129 129 \n")# The grid dimensions
        fp.write("       nlev 4 \n")# Multigrid level parameter
        fp.write("       gcent mol 3 \n")# Center the grid on molecule 1
        fp.write("       lpbe \n")# Solve the linearized Poisson-Boltzmann
        fp.write("       bcfl mdh \n")# Use all multipole moments when calculating the
        fp.write("       pdie 1.0 \n")# Solute dielectric
        fp.write("       sdie 80 \n")# Solvent dielectric
        fp.write("       chgm spl2 \n")# Spline-based discretization of the delta functions
        fp.write("       ion 1 0 1.33\n")
        fp.write("       srfm mol \n")# Molecular surface definition
    if TYPE=="NSP":
        fp.write("apolar name 1_solv\n") #Calculate potential for reference (vacuum) state
        fp.write("       srfm sacc\n")
    	fp.write("       dpos 1.0\n")
    	fp.write("       press 0.0\n")
        fp.write("       gamma  	0.021\n")
        fp.write("       bconc 0\n")


    fp.write("       mol 1 \n")# Perform the calculation on molecule 1
    fp.write("       grid 0.5 0.5 0.5 \n") # Grid spacing
    fp.write("       srad 1.4 \n")# Solvent probe radius (for molecular surface)
    fp.write("       swin 0.3 \n")# Solvent surface spline window (not used here)
    fp.write("       sdens 10.0\n")
    fp.write("       temp %d \n" %temp)# Temperature
    fp.write("       calcenergy total \n")# Calculate energies
    fp.write("       calcforce no \n")# Do not calculate forces
    fp.write("end\n")

    fp.write("print\n") 
    fp.write(" 	energy 1_solv\n") 
    fp.write("end\n")
    fp.write("quit\n")

def Create_PDB(coor_file,traj_file,index_file,out_file,group_index,skip):
    commd="Trjconv.py -p %s -f %s -n %s -o %s --skip %d\n" %(coor_file,traj_file,index_file,out_file,skip)
    pf=Popen(commd,stdin=PIPE,stdout=PIPE,stderr=STDOUT,shell=True)  
    pf.stdin.write("%d\n"%group_index)
    print "Waiting for calculating the eigenvalue and eigenvector files......"
    pf.wait()

#    print pf.stdout.read()
    print "It's finished! "

def Create_PQR(coor_prefix):



       

if __name__ =='__main__':
    Write_mdp("test.mdp")
    Write_apbs("test_sp.in","pqrfile",TYPE="SP")
    Write_apbs("test_nsp.in","pqrfile",TYPE="NSP")

 #  a Checkargs()



