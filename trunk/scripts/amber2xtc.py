#!/usr/bin/python
"""
v0.1 2012.04.20
"""

#from MDAnalysis.tests.datafiles import PRMpbc,TRJpbc_bz2
#from MDAnalysis.tests.datafiles import PRM,TRJ_bz2
from MDAnalysis import Universe, Writer
from MDAnalysis.core.util import greedy_splitext

import os.path
import sys

def echo(s=''):
    """Simple string output that immediately prints to the console."""
    sys.stderr.write(s)
    sys.stderr.flush()

if __name__=="__main__":
    TRJ_LEN=len(sys.argv)
    if TRJ_LEN < 3:
        print "Error"
        sys.exit()

    topol =sys.argv[1] #PRMpbc
    TRJ_LIST=list()
    for i in range(TRJ_LEN-2):
        TRJ_LIST.append(sys.argv[2+i])

    outtrj = "traj.xtc"


    # create a writer instance for the output trajectory
    print "Reading trajectory %s" %TRJ_LIST[0]
    u = Universe(topol, TRJ_LIST[0])
    w = Writer(outtrj, u.trajectory.numatoms)
    FRAME=0

    for j in range(len(TRJ_LIST)):
        if u.trajectory.dt==0.0:
            print "No time step information found in the trajectoy file."
            DT=raw_input("Input a float number for the time step:")
            u.trajectory.dt=float(DT)
        else:
            print "Time step %6.4f was found and will be used in the new trajectory." %u.trajectory.dt
        for ts in u.trajectory:
            FRAME=FRAME+1
            ts.time=(FRAME-1)*u.trajectory.dt
            w.write(ts)
            if FRAME %100==0:
                echo("Converted frame %8d ,time %8.2f\r" %(ts.frame,FRAME*u.trajectory.dt))
        if j < len(TRJ_LIST)-1:
            print ""
            print "Reading trajectory %s" %TRJ_LIST[j+1]
            u = Universe(topol, TRJ_LIST[j+1])
    w.close()
    print "Writing the result file traj.xtc finished."

