=================
File format list
=================

PDB
======

Introduction to Protein Data Bank Format
----------------------------------------

Protein Data Bank (PDB) format is a standard for files containing atomic coordinates. Structures
deposited in the Protein Data Bank at the Research Collaboratory for Structural Bioinformatics (RCSB) are
written in this standardized format. The short description provided here will suffice for most users. How-
ever, those actually creating PDB files should consult the definitive description (see
http://www.rcsb.org/pdb/info.html#File_Formats_and_Standards).

The complete PDB file specification provides for a wealth of information, including authors, literature 
references, and the identification of substructures such as disulfide bonds, helices, sheets, and active
sites. Users should bear in mind that modeling programs can be unforgiving of incorrect input formats.

Description
------------

+-----------+----------+-------------------------------------+---------------+-------------+ 
|Record Type| Columns  |   Data                              |  Justfication | DataType    |
+===========+==========+=====================================+===============+=============+
| ATOM      |   1-4    |  "ATOM"                             |   left        |    character|
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           |   7-11   |  Atom serial number                 |   right       |  integer    |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           |  13-16   | Atom name                           | left*         |  character  |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           |   17     |  Alternate location indicator       |               | character   |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           |  18-20   | Residue name                        |  right        | character   |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           |  22      | Chain identifier                    |               |  character  |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           |  23-26   | Residue sequence number             |  right        | integer     |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           |  27      | Code for insertions of residues     |               | character   |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           |  31-38   | X orthogonal Angstrom coordinate    |   right       | floating    |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           |  39-46   | Y orthogonal Angstrom coordinate    |   right       | floating    |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           | 47-54    | Z orthogonal Angstrom coordinate    |   right       | floating    |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           | 55-60    | Occupancy                           | right         | floating    |           
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           | 61-66    | Temperature factor                  | right         | floating    |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           | 73-76    | Segment identifier (optional)       |    left       | character   |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           | 77-78    | Element symbol                      | right         | character   |
+-----------+----------+-------------------------------------+---------------+-------------+ 
|           | 79-80    | Charge (optional)                   |               |   character |
+-----------+----------+-------------------------------------+---------------+-------------+ 




PQR
======

This format is a modification of the PDB format which allows users to add charge
and radius parameters to existing PDB data while keeping it in a format amenable 
to visualization with standard molecular graphics programs. The origins of the PQR 
format are somewhat uncertain, but has been used by several computational biology 
software programs, including MEAD and AutoDock. UHBD uses a very similar format 
called QCD.

APBS reads very loosely-formatted PQR files: all fields are whitespace-delimited 
rather than the strict column formatting mandated by the PDB format. This more 
liberal formatting allows coordinates which are larger/smaller than ± 999 Å.

APBS reads data on a per-line basis from PQR files using the following format:

-------------------------

 Field_name Atom_number Atom_name Residue_name Chain_ID Residue_number X Y Z Charge Radius

-------------------------

where the whitespace is the most important feature of this format. The fields are:

- Field_name

  A string which specifies the type of PQR entry and should either be ATOM or HETATM in order to be parsed by APBS.

- Atom_number

  An integer which provides the atom index.

- Atom_name

  A string which provides the atom name.

- Residue_name

  A string which provides the residue name.

- Chain_ID

  An optional string which provides the chain ID of the atom. Note chain ID support is a new feature of APBS 0.5.0 and later versions.

- Residue_number

  An integer which provides the residue index.

- X Y Z

  3 floats which provide the atomic coordiantes.

- Charge

  A float which provides the atomic charge (in electrons).

- Radius

  A float which provides the atomic radius (in Å).

Clearly, this format can deviate wildly from PDB due to the use of whitespaces 
rather than specific column widths and alignments. This deviation can be 
particularly significant when large coordinate values are used. However, in order 
to maintain compatibility with most molecular graphics programs, the PDB2PQR 
program and the utilities provided with APBS (see the Parameterization section) 
attempt to preserve the PDB format as much as possible.



GRO
======

Files with the gro file extension contain a molecular structure in Gromos87 format. gro files 
can be used as trajectory by simply concatenating files. An attempt will be made to read a 
time value from the title string in each frame, which should be preceded by 't=', as in the 
sample below.

A sample piece is included below:

-----------------------

MD of 2 waters, t= 0.0

6

1WATER  OW1    1   0.126   1.624   1.679  0.1227 -0.0580  0.0434

1WATER  HW2    2   0.190   1.661   1.747  0.8085  0.3191 -0.7791

1WATER  HW3    3   0.177   1.568   1.613 -0.9045 -2.6469  1.3180

2WATER  OW1    4   1.275   0.053   0.622  0.2519  0.3140 -0.1734

2WATER  HW2    5   1.337   0.002   0.680 -1.0641 -1.1349  0.0257

2WATER  HW3    6   1.326   0.120   0.568  1.9427 -0.8216 -0.0244

1.82060   1.82060   1.82060

----------------------------


Lines contain the following information (top to bottom):

- title string (free format string, optional time in ps after 't=')
- number of atoms (free format integer)
- one line for each atom (fixed format, see below)
- box vectors (free format, space separated reals), values: v1(x) v2(y) v3(z) 
  v1(y) v1(z) v2(x) v2(z) v3(x) v3(y), the last 6 values may be omitted (they will 
  be set to zero). Gromacs only supports boxes with v1(y)=v1(z)=v2(z)=0.


This format is fixed, ie. all columns are in a fixed position. Optionally (for now only 
yet with trjconv) you can write gro files with any number of decimal places, the format 
will then be n+5 positions with n decimal places (n+1 for velocities) in stead of 8 with 
3 (with 4 for velocities). Upon reading, the precision will be inferred from the distance 
between the decimal points (which will be n+5). Columns contain the following information 
(from left to right):

- residue number (5 positions, integer)
- residue name (5 characters)
- atom name (5 characters)
- atom number (5 positions, integer)
- position (in nm, x y z in 3 columns, each 8 positions with 3 decimal places)
- velocity (in nm/ps (or km/s), x y z in 3 columns, each 8 positions with 4 decimal places)

Note that separate molecules or ions (e.g. water or Cl-) are regarded as residues. If you want 
to write such a file in your own program without using the GROMACS libraries you can use the 
following formats:

C format

    "%5d%5s%5s%5d%8.3f%8.3f%8.3f%8.4f%8.4f%8.4f"


XYZ
======

The XYZ file format is a chemical file format. There is no formal standard and several 
variations exist, but a typical XYZ format specifies the molecule geometry by giving the 
number of atoms with Cartesian coordinates that will be read on the first line, a comment 
on the second, and the lines of atomic coordinates in the following lines. The file format 
is used in computational chemistry programs for importing and exporting geometries. The 
units are generally in Ångströms. Some variations include using atomic numbers instead of 
atomic symbols, or skipping the comment line. Files using the XYZ format conventionally 
have the .xyz extension.

Format
--------

The formatting of the .xyz file format is as follows:

---------------------

<number of atoms>

comment line

atom_symbol1 x-coord1 y-coord1 z-coord1

atom_symbol2 x-coord2 y-coord1 z-coord2

...

atom_symboln x-coordn y-coordn z-coordn

-------------------


Example
--------

The methane molecule can be described in the XYZ format by the following:

------------------

5

methane molecule (in [[Ångström]]s)

C        0.000000        0.000000        0.000000

H        0.000000        0.000000        1.089000

H        1.026719        0.000000       -0.363000

H       -0.513360       -0.889165       -0.363000

H       -0.513360        0.889165       -0.363000

------------------


amber TOP
=========

amber CRD
=========

