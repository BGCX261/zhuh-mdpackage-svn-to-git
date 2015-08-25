==================
Parallel_analysis
==================

---------------
Introduction
---------------


Parallel analysis.py is used for calculate the distance and angle between two
bases groups. usually a group contain 1, 2 or 4 bases in a plane.
The angle is useful to analysis the base stack. Two stack bases usually have a
small angle and 
uctuation.
If the opition "--rmsd" used, only one bases group will be selected and the RMSD
in z-axis for this group will be calculated.

------------
Usage
------------


**Files**

========  ======  ===========  ================================
Option    Type    Filename     Description
========  ======  ===========  ================================
-p        Input   coor_file    Structure fie: gro pdb etc.
-f        Input   traj_file    Trajectory: xtc trr.
-o        Input   output_file  xvgr/xmgr file.
-i        Input   para_an.in   input parmarter file.
========  ======  ===========  ================================

**Other options**

========  ======  ===========  ============================================
Option    Type    Value        Description
========  ======  ===========  ============================================
--rmsd    bool    False        skip Calculate the RMSD of DNA bases groups.
--skip    int     1            Get frames when frame MOD skip = 0
-h        bool    yes          Print help info and quit
========  ======  ===========  ============================================

-----------------------------
Some details of the Algorithm
-----------------------------
