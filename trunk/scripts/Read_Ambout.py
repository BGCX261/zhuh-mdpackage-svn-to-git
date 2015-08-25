#!/usr/bin/env python

import sys
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import time


def Fit(data_in, data_out="Output.xvg",isPlot=False):

    if not os.path.isfile(data_in):
        print "file %s not found." %data_in
        sys.exit(0)

    fr=open(data_in, 'r')

    if not isPlot:
        fw=open(data_out,'w')

    lines=fr.readlines()
    new_line=""
    WRITE_TITLE=True
    START=False

    Big_matrix=list()

    for line in lines:
        if "NSTEP" in line:
            START=True
            if new_line != "":
                temp_line=""
                temp_list=list()
                if WRITE_TITLE==True:
                    temp_line="#"
                te=re.split('\s+',new_line)
                while te.count("=") > 0:
                    a=te.index("=")
                    if WRITE_TITLE==True:
                        temp=""
                        for ss in range(a+2):
                            if ss < a:
                                temp=temp+" "+te.pop(0)
                            else:
                                te.pop(0)
                        temp_line=temp_line+"%12s" %temp
                    if  WRITE_TITLE==False:
                        for ss in range(a+2):
                            if ss == a+1:
                                aaaa=te.pop(0)
                                if isPlot:
                                    temp_list.append(float(aaaa))
                                else:
                                    temp_line=temp_line+"%12s" %aaaa
                            else:
                                te.pop(0)
                WRITE_TITLE=False

                if isPlot:
                    if len(temp_list)>0:
                        Big_matrix.append(temp_list)
                else:
                    fw.write("%s\n" %temp_line)

            new_line=""
            new_line=new_line+line[:-1]
        elif START:
            new_line=new_line+line[:-1]
    fr.close()
    if not isPlot:
        fw.close()

    if isPlot:
        return Big_matrix

def Usage():
    print "Read_ambout.py md.out result.xvg isPlot(Yes/No)"


def Plot(input_file,xy_list):
    plt.ion()

    while True:
        r = np.array(Fit(input_file,isPlot=True)) 

        ax = plt.gca()
        for xy in xy_list:
            ax.plot(r[:,xy[0]-1], r[:,xy[1]-1],)

        plt.draw()
        time.sleep(10)
        plt.clf()


if __name__ =="__main__":
    if len(sys.argv) == 4:
        isPlot=sys.argv[3]
        if isPlot=="No":
            Fit(sys.argv[1],sys.argv[2],False)
        if isPlot=="Yes":
            xylist=list()
            while True:
                xy=raw_input("input chromn number for xy(Enter to break):")
                xy=[int(a) for a in xy.split()]
                if len(xy)==0:
                    break
                xylist.append(xy)
            print xylist

            Plot(sys.argv[1],xylist)

    else:
        Usage()
        sys.exit()

