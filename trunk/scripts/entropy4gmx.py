#! /usr/bin/env python
'''
@author: zhuh 
@change:\n
    - V 0.1.0 finished at2010.11.04\n
        - it's runing now. but coundn't make  sure it make the right result.\n  
    - V 0.1.1 update at 2010.11.07\n
        - Using the subprocess.Popen to run the g_cover the result is the same
        with Qhentropy. which is write by zhuh using C++ to do the same thing.
    - V 0.2.0 update at 2010.11.27\n
        - Change the traj_time to  begin time and end time. so it's possable to 
        calculate the entropy using only a part of the trajout. 
        - it's check if the trajout file and tpr file exists now.
    - V 0.2.1 update at 2011.01.04\n
        - now it's aviliable for multgroups.
    - V 0.2.2 update at 2012.06.04\n
        - More help informations add. Some optimization also add.
    - V 0.3.0 update at 2012.09.20\n
        - Contain the algorithm in Qhentropy.
    - V 0.3.1 update at 2012.10.07\n
        - More optimization.
'''

import string
import sys
import os
import re
import math
import subprocess
from subprocess import Popen, PIPE, STDOUT
import getopt
#from MDPackage import usage
    
K= 1.3806504e-23
'''It's the Boltzmann constant'''
HBA= 1.05457148e-34
'''It's the Planck constant'''
R= 8.3145
'''It's the idea gas constant'''
E= 2.71828183
'''natural exp poment e'''
MP=1.66055402e-27
'''1 a.m.u. = Proton mass [kg] '''
CYCLE=20
'''the number of the bins'''
    
def Checkargs():
    eigenfile=""
    temperature=300.0
    algorithm="A"
    input_file=""
    opts,args=getopt.getopt(sys.argv[1:],"hvi:f:t:c:")
    for a,b in opts:
        if a =="-i":
            input_file=b
        elif a =="-f":
            eigenfile=b
        elif a == "-t":
            temperature = float(b)
        elif a == "-c":
            algorithm= b
        elif a == "-v":
            Usage(True)
            sys.exit()
        elif a =="-h":
            Usage()
            sys.exit()
        else:
            Usage()

    if os.path.isfile(input_file):
        my_hash=Read_input(input_file)
        Calculate_entropy(my_hash)
    elif os.path.isfile(eigenfile):
        eigval_list=Read_eigenval(eigenfile)
        entropy=Get_Entropy(eigval_list,temperature,algorithm)
        print "\tTemperature: %10.1f K" %temperature
        print "\tAlgorithm: %3s"    %algorithm
        print "\tThe entropy: %10.3f J/mol/K, %10.3f Kcal/mol." %(entropy,entropy*temperature/4200)
        
def Usage(loud=False):
    '''Print the usage information'''
    print    "Usage : entropy2gmx.py -i <input file>"
    print    "        entropy2gmx.py -f <eigenfile> -t temperature -c algorithm[A/S]"
    print    "options:"
    print    "\t -h\t bool\t\t no\t Print help infomation and quit."
    print    "\t -v\t bool\t\t no\t Be loud and noisy."
    print    "\t -i\t input.in\t Input\t Set input file."
    print    "\t -f\t eigenfile.xvg \t Input\t eigenvalue file."
    print    "\t -t\t temperature\t Input\t temperature."
    print    "\t -c\t algorithm[A/S]\t Input\t algorithm, A for Andricicaei and S for Schlitter."

    if loud == True:
        print "="*50
        print "Input Example"
        print "="*50
        print "#Input and Output control"
        print "traj_name       traj.xtc"
        print "index_name      index.ndx"
        print "target_group    name1 name2 name3    #Multiple groups are allowed. "
        print "reference_group name1 name2 name3    #Multiple groups are allowed. If not defined, "
        print "                                     #the target group will be used as reference."
        print "tpr_name        md.tpr"
        print 
        print "begin_time      0   #Unit is ps."
        print "end_time        10000"
        print ""
        print "out_file        out_1.xvg out_2.xvg out_3.xvg"
        print ""
        print "#calculate parameters"
        print "Temp            300 #the unit is K"
        print "Algorithm       Andricicaei  #Just 'Andricicaei' and 'Schlitter' allowed. default is 'Andricicaei'"
        print "clean           False        #If true, the eigenvector files will be delete after the calculation finished."


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
                my_hash["begin_time"]=int(line_units[1])

            elif line_units[0] == "end_time":
                my_hash["end_time"]=int(line_units[1])    

            elif line_units[0] == "out_file":
                for count in range(len(line_units)):
                    if string.find(line_units[count],'#')>-1:
                        my_hash["out_file"]=line_units[1:count]
                        break 
                    else:
                        my_hash["out_file"]=line_units[1:count]              

            elif line_units[0] == "Temp":
                my_hash["Temp"]=float(line_units[1])

            elif line_units[0] == "Algorithm":
                my_hash["Algorithm"]=line_units[1]

            elif line_units[0] == "tpr_name":
                if os.path.isfile(line_units[1]):
                    my_hash["tpr_name"]=line_units[1]
                else:
                    print "Error:the tpr file not exist!"
                    exit(2)

            elif line_units[0] == "target_group":
                for count in range(len(line_units)):
                    if string.find(line_units[count],'#')>-1:
                        my_hash["target_group"]=line_units[1:count]
                        break
                    else:
                        my_hash["target_group"]=line_units[1:count]

            elif line_units[0] == "reference_group":
                for count in range(len(line_units)):
                    if string.find(line_units[count],'#')>-1:
                        my_hash["reference_group"]=line_units[1:count]
                        break
                    else:
                        my_hash["reference_group"]=line_units[1:count]

            elif line_units[0] == "clean":
                my_hash["clean"]=line_units[1]

    # print my_hash    

    if my_hash.has_key('traj_name')==False:
        print "need parameter traj_name"
        sys.exit()
    if my_hash.has_key('index_name')==False:
        print "need parameter index_name"
        sys.exit()
    if my_hash.has_key('begin_time')==False:
        print "need parameter begin_time"
        sys.exit()
    if my_hash.has_key('end_time')==False:
        print "need parameter end_time"    
        sys.exit()
    if my_hash.has_key('out_file')==False:
        print "need parameter out_file"
        sys.exit()
    if my_hash.has_key('Temp')==False:
        print "need parameter Temp"
        sys.exit()
    if my_hash.has_key('Algorithm')==False:
        print "need parameter Algorithm"
        sys.exit()
    if my_hash.has_key('tpr_name')==False:
        print "need parameter tpr_name"
        sys.exit()
    if my_hash.has_key('target_group')==False:
        print "need parameter target_group"
        sys.exit()
    if my_hash.has_key('reference_group')==False:
        my_hash['reference_group']=my_hash['target_group']

    if my_hash.has_key('clean'):
        if my_hash['clean']=="True":
            my_hash['clean']=True
        else:
            my_hash['clean']=False
    else:
        my_hash['clean']=False


    print "Finish reading all parameters."

    print "Checking g_covar."
    Check_commd("g_covar")
        
    return my_hash

def Read_index(index_file_name):
    '''It's read the index file to return a hash target_group->group_index.'''
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
               
def Calculate_entropy(hash_name):
    '''It's the core function. get the infromation form traj file and calculate
    the entrpoies.'''
    global CYCLE
    index_name=hash_name["index_name"]
    index_hash=Read_index(index_name)

    tpr_name=hash_name["tpr_name"]
    traj_name=hash_name["traj_name"]
    begin_time=hash_name["begin_time"]

    
    for i,target in enumerate(hash_name["target_group"]):
        out_file=hash_name["out_file"][i]
        if os.path.isfile(out_file):
            try:
                os.rename(out_file,"#"+hash_name["out_file"]+"#")
            except:
                print "Warning: the file %s will be overwrite." %out_file
        try:
            out_put=open(out_file,'w+')
        except:
            print sys.exc_info()[1]

        try:
            target_index    =index_hash[target]
            reference_index =index_hash[hash_name['reference_group'][i]]
        except:
            print "Error: ", sys.exc_info()[1]," was not found in index file. Please check it first."
            sys.exit()
        out_put.write("#Target group   :"+target+"\n")  #out put 
        out_put.write("#Reference group:"+hash_name["reference_group"][i]+"\n")
        out_put.write("#Time\t\tEntropy\n")          #out put 
        out_put.write("@\t title \t"+'''"Entropy"\n''')
        out_put.write("@\t xaxis \t label "+'''"Time (ps)"\n''')
        out_put.write("@\t yaxis \t label "+'''"Entropy (J/mol/K)"\n''')
        
    
        for i in range(CYCLE):
            end_time=(hash_name["end_time"]-begin_time)/CYCLE*(i+1)+begin_time
            eigval_name="eigenval_"+target+"_%d" %(i+1)
            commd= "g_covar -s %s -f %s -n %s -b %d -e %d -mwa -o %s -v %s -av %s -l %s" \
            %(tpr_name,traj_name,index_name,begin_time,end_time,eigval_name,eigval_name,eigval_name,eigval_name)
            # comd="g_covar -s "+tpr_name+" -f "+traj_name
            # comd+=" -n "+index_name+" -b "+begin_time+" -e "
            # comd+= "%d" %end_time+" -mwa -o "+eigval_name+" -v "
            # comd+=eigval_name+" -av "+eigval_name+" -l "+eigval_name

            Run_commd(commd,target_index,reference_index,i+1)	

            if hash_name['clean']==True:
                filename=eigval_name+".trr"
                os.remove(filename)
                print "\tDelete file %s" %filename

            eigenval_list=Read_eigenval(eigval_name+".xvg")
            if hash_name["Algorithm"]=="Andricicaei":
                entropy=Get_Entropy(eigenval_list,hash_name["Temp"],"Andricicaei")
            elif  hash_name["Algorithm"]=="Schlitter":
                entropy=Get_Entropy(eigenval_list,hash_name["Temp"],"Schlitter")
            else:
                print "Error: input a wrong algorithm, only Andricicaei or Schlitter allowd."
                exit()

            out_put.write("%d\t\t%f\n" %(end_time,entropy)) #out put
                
        print "\tWritting the results to the file %s\n" %out_file
        out_put.close()
    
def Run_commd(commd,traget_ID,reference_ID,circle_index):
    '''Just used to run commd by Popen.'''
    pf=Popen(commd,stdin=PIPE,stdout=PIPE,stderr=STDOUT,shell=True)  
    pf.stdin.write("%d\n"%reference_ID)
    pf.stdin.write("%d\n"%traget_ID)

    print "Cycle %s" %circle_index
    sys.stdout.write("\tWaiting for calculating the eigenvalue and eigenvector files......")
    sys.stdout.flush()
    pf.wait()

#    print pf.stdout.read()
    print "\tDone! "

def Check_commd(commd):
    try:
        a=subprocess.check_output(["which",commd])
        print "\t%s will be used." %a.strip()
    except:
        print "%s not found." %commd
        sys.exit()


def Get_Entropy(eigval_list,temperature=300,algorithm="Andricicaei"):
    '''The Andricicaei Algorithm.'''
    global R
    global K
    global E
    global HBA
    global MP
    omiga = HBA*(1e9)/math.sqrt(K*temperature*MP)
    apart = [omiga/math.sqrt(temp) for temp in eigval_list]
    if algorithm=="Andricicaei" or algorithm  =="A":
        tempQ = [ap/(math.exp(ap)-1) - math.log(1-math.exp(-ap)) for ap in apart]
    elif algorithm=="Schlitter" or algorithm == "S":
        tempQ = [math.log(1+math.pow(E/ap, 2)) for ap in apart]
    entropy = sum(tempQ) * R
    return entropy


def Read_eigenval(eigenval_file):
    '''Read the eigenvalue file and return a list. just 1/3 of the eigenvalues will
    be returned.'''
    eigenval_list=[]
    try:
        fh=open(eigenval_file,'r')
    except:
        print eigenval_file,":",sys.exc_info()[1]
        print "It means that the program 'g_covar' not work well. So, you should check it first."
        sys.exit()
    while True:
        aline=fh.readline()
        if aline !="":
            if (aline.find('#')>-1 or aline.find('@')>-1):
                continue
            else:
                eigenval_list.append(string.atof(re.split('\s+',aline)[2]))
                if eigenval_list[-1] < 0.000001:
                    break
                else:
                    continue
        else:
            break
    print "\t%d eigenvalues used" %(len(eigenval_list)-1)
    return eigenval_list[:-1]
       

if __name__ =='__main__':
    Checkargs()
