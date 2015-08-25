#-*- coding: utf-8 -*-
'''
Created on 2011-01-19.
Created for calculated the average of the date in a row.
@change:\
    - 2011-01-19\
        - It's test OK
'''
import math
import re
import string
from numpy import array , dot

def Calculate_average(num_list):
    n=len(num_list)
    ave=sum(num_list)/n
    num_array=array(num_list)
    var=dot( num_array-ave ,num_array-ave )/n
    svar=math.sqrt(var)
    resu=[ave,svar]
    return resu

def Read_data_4_averge(data_name,row):
    fp = open(data_name,"r+")
    lines = fp.readlines()
    num_list=[]
    for line in lines:
        if "#" not in line:
            line_units=re.split("\s+",string.strip(line))
#        print line_units
            try:
                num_list.append(float(line_units[row-1]))
            except:
                print "read a string %s , ignored" %line_units[row-1] 
                pass
    result=Calculate_average(num_list)       
    return result



