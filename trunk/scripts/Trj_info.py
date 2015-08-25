#!/usr/bin/env python
'''
It's a small script used to show details of the XDR file.
'''

import MDAnalysis 
import sys
import os.path

def Read_traj(file_name):
    if file_name.endswith(".xtc"):
        Traj=MDAnalysis.coordinates.xdrfile.XTC.XTCReader(file_name)
    elif file_name.endswith(".trr"):
        Traj=MDAnalysis.coordinates.xdrfile.TRR.TRRReader(file_name)
    else:
        print "The format of %s is invalid." %file_name
        sys.exit()

    print "Details of the trajectory file %s" %file_name
    print "File name:    %s" %os.path.basename(file_name)
    print "Atom number:  %d" %Traj.numatoms
    print "Frame number: %d" %Traj.numframes
    print "Delta:        %.3f ps" %Traj.delta
    print "Total time:   %.3f ps" %Traj.totaltime

    Traj.close()

def Usage():
    print "Usage: Trj_info.py XDR_file_name"


if __name__=="__main__":
    if len(sys.argv)==2:
        Read_traj(sys.argv[1])
    else:
        Usage()

