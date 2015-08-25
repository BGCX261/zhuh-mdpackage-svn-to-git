#! /usr/bin/env python

import sys
import os
import getopt

def Checkargs():
    argc=len(sys.argv)
    pqr_file=""
    in_file=""
    out_file=""
    if argc != 7:
        Usage()
        exit()
    for i in range(7):
        opts,args=getopt.getopt(sys.argv[1:],"hf:i:o:")
        for a,b in opts:
            if a=="-f":
                if os.path.isfile(b):
                    pqr_file=b
                else:
                    print "file %s not exist!" % b
                    sys.exit(0)
            if  a=="-i":
                if os.path.isfile(b):
                    in_file=b
                else:
                    print "file %s not exist!" % b
                    sys.exit(0)
            if  a=="-o":
                out_file=b
            
    pdb2pqr(pqr_file,in_file,out_file)

def pdb2pqr(pqr_file,in_file,out_file):
    pqr_file=hash_name["pqr_file"]
    in_file=hash_name["in_file"]
    out_file=hash_name["out_file"]
    seg_list=[]
    i=0
    try:
        fh1=open(pqr_file,'r')
        fh2=open(in_file,'r')
        fh3=open(out_file,'w+')
    except:
        pass
    
    while True:
        lin1=fh1.readline()
        if lin1 != "":
            if ("ATOM" in lin1) or ("HETATM" in lin1):
                seg_list.append(lin1[54:])
            else:
                pass
        else:
            break
                        
    while True:
        lin2=fh2.readline()
        
        if lin2 != "":
            if ("ATOM" in lin2) or ("HETATM" in lin2):
                fh3.write(lin2[:54])
                fh3.write(seg_list[i])
                i+=1
            else:
                fh3.write(lin2)
        else:
            break
                                     
    fh1.close()
    fh2.close()
    fh3.close()
    print "finished write the file %s" % out_file
    

def Usage():
    print "Usage: my_pdb2pqr.py -f ligand.pqr -i pdb_input.pdb -o out.pqr"


if __name__ =='__main__':
    Checkargs()
