==========
Change log 
==========

About
------
This file is design for write the change of this program.

2011-12-26
----------
- Modified some functions in **Simple_atom** module.
- Modified the **Trj_modify.py** script. It now can move the solvate to the origin postion in the
  first frame.

2011-09-20
----------
- Add the version to 0.0.9
- Add some files in script, about convert trajectory files.


2011-08-23
----------
- Add the version to 0.0.8.
  add a module named amber_top.py. which used to read in the amber top file. and modified 
  the Simple_atom.py PDB.py GRO.py. Delete some not used functions. Move the Simple_atom 
  class to a new file named unit_atom.py. and the name of the class is unit_atom. 
- Now, only Simple_atom module will be used by other modules. and the PDB , GRO module while
  only be used by Simple_atom.
- Parallel_analysis can be used for amber trajectory.
2011-05-11
----------
- Fixed a problem in parallel_analysis.py. about calculate the RMSD-Z for a bases group.


2011-04-02
----------
- write a function named echo, which usage for print and flush.

2011-03-20
----------
- writes some functions for calculate the RMSD of bases group

2011-03-18
----------
- rewrite some functions in parallel_analysis

2011-03-16
----------
- Fixed a problem in Index.py.

2011-03-07
----------
- Change the version to 0.0.7
- Add the entropy4gmx.py to scripts.

2011-02-28
----------
- Add module PQR in MDPackage package. It's used for read in a one or more pqr file and put
  them together.
- Modified the Modify_Coor script. It read in a pqr file, check it and save it to another
  pqr file.

2011-02-25
----------
- Modified the script Modify_Coor.py, It's runing now.

2011-02-24
----------
- Add **entropy4gmx.py** to scripts.


2011-02-23
----------
- Optimiztied the function **Traj_2_coor()** in Traj module and the script **Trjconv.py**.

2011-02-22
----------
- Modified a bug in Index module.
- Add a script named **Trjconv.py**. It's used for convert a trajectory file to a list of 
  structure file using the function **Traj_2_coor()** in Traj module.

2011-02-21
----------
- Modified some bugs in Simple_atom module.
- Add a function **Traj_2_coor()** in Traj module. It's read in a trajectory file and write
  frames to structure files like \*.gro or \*.pdb

2011-02-20
----------
- Modified a bugs in **Index** class. Now in a index list, the list[0] is named *system*.
- Modified the Modify_Coor.py. Now loading a molecular, delete groups and saving it is
  aviliable.


2011-02-18
----------
- Modified a bug in Index.py, change *reside* to *residue*.
- Add some code in Modify_Coor.py for the command mode, run as **Modify_Coor.py -f <filename1> 
  -o <filename2>**, It's runing now, but some necessary code are instead by **pass**.

2011-02-17
----------
- Modified the Simple_atom class, add atom_2_PDBformat() and atom_2_GROformat() functions.



2011-02-16
----------
- Add **Atomlist_2_Index()** in Index module. This function is used to Create a group list
  from a atom list which read from a structure file like gro or pdb.
- Created a script file named Modify_Coor.py. which is used to load a structure file and 
  modified it , like delete some groups or save a index file etc. It's not finished now.
- Rewrite the output of PDB format for the atom name.
- Created functions for PDB format convert to GRO format and GRO format convert to PDB format. 
- Change the version to 0.0.6

2011-02-15
----------
- Change the time scale from frame to ns in Parallel_analysis and Twist_in_GDNA.



2011-02-12
-----------
- Modified the Twist_in_GDNA.py, Using the getopt to analysis the input command arguments.

2011-02-01
-----------
- Finished the function **Get_Segment_list()** in GRO.py.
- Modified the module parallel_analysis.py, so both gro file and pdb file are allowd for 
  coordinate input.
- Modified the script file Parallel_analysis.py, so both gro file and pdb file are allowd for 
  coordinate input.
- Change the version to 0.0.5.

2011-01-25
-----------
- Add the Simple_atom class, which contain the atom coordinate and atom sequence information.
  so gro and pdb file all can be used in twist_in_GDNA. parallel_analysis also will be changed.
- parallel_analysis not finished.

2011-01-24
-----------
- Add the test_da.py to test.py. So the test file can used to test every function.

2011-01-23
----------
- Finish the function Get_Atom_list() in GRO.py module, and test it in test.py.

2011-01-22
-----------
- Create file GRO.py in MDPackage package. But it's not finished.
- Modified the Parallel_analysis.py. Make it check if the input is 
  invalid.


