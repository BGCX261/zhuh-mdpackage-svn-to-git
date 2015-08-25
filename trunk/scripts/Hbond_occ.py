#!/usr/bin/env python
'''
It's a scripy to calculate the occupied of hbond of the data from vmd hbond.
'''

import sys
import string

def Run_occ(hb_file,resu_file,dt):
    _STEP=50
    fr=open(hb_file,'r')
    fw=open(resu_file,'w')

    all_lines=fr.readlines()
    fr.close()

    NUM=len(all_lines)
    for k in range(NUM-_STEP):
        occ=0.0
        for i in range(_STEP):
            occ=occ+float(string.split(all_lines[k+i])[1])
        occ=occ/_STEP
        time=(k+_STEP/2)*dt
        fw.write("%8.4f    %6.3f\n" %(time,occ))
    fw.close()
    print "Finish write the result to %s" %resu_file



if __name__=="__main__":
    if len(sys.argv)==4:
        hb_file=sys.argv[1]
        resu_file=sys.argv[2]
        dt=float(sys.argv[3])
    else:
        print "Usage: Hbond_occ hb_file resu_file dt"
        sys.exit()

    Run_occ(hb_file,resu_file,dt)

