===========
Trj_modify
===========

------------
Introduction
------------
Trj_modify is design for fit the trajectory to the first frame by translation and rotation. First it move the solvate to the ceter, then it fit to the first frame of the trajectory.

------------
Usage
------------
**Trj_modify topology_file  trajectory_file  output_trajectory_file**

Input trajectory file can be in any format support by **MDAnalysis**, and the suggest output format of trajectory file is *xtc*,

.. warning::
    This program will read the pbc condition and use the dimensions read from trajectory files. You should make sure the dimensions are right or it will create a wrong output trajectory file.



-------------------------------
Some detials of the Algorithm
-------------------------------

