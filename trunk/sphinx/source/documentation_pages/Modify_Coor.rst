====================
Modify_Coor
====================


--------------------
Introduction
--------------------

Modify_Coor convert a structure file from one format to another or modified
the structure file. The structure file can be in pdb, gro or pqr format.

---------------
Usage
---------------

Interactive Mode
----------------

**Modify_Coor.py** to run interactive mode.
Type help can see the list of the key words. They are listed below.

+----------+----------------+-----------------------------------------------------+
|load      | < filename >   |  : Load a structure file: gro pdb etc.              |
+----------+----------------+-----------------------------------------------------+
|list      |                |   : List the groups.                                |
+----------+----------------+-----------------------------------------------------+
|<Enter>   |                |   : List the groups.                                |
+----------+----------------+-----------------------------------------------------+
|delete    |< groupname >   |  : Delete a group.                                  |
+----------+----------------+-----------------------------------------------------+
|splitres  |< groupname >   | : Split a group to residues.                        |
+----------+----------------+-----------------------------------------------------+
|splitatom | < groupname >  | : Split a group to atoms.                           |
+----------+----------------+-----------------------------------------------------+
|save      | < filename >   | : Save the result to a structure file: gro pdb etc. |
+----------+----------------+-----------------------------------------------------+
|history   |                | : Print the input history.                          |
+----------+----------------+-----------------------------------------------------+
|help      |                | : Print help information.                           |
+----------+----------------+-----------------------------------------------------+
|quit      |                | : Quit                                              |
+----------+----------------+-----------------------------------------------------+

**load** 

Now many structure file format are allowed to load, include gro, pdb, pqr and amber top+crd.

**save**

Only two types of the structure file format (pdb and gro) can be saved by this program.


Commond Mode
-------------

**Modify_Coor.py -f filename -o filename** to run interactive mode.


-------------
Some Detials
-------------
