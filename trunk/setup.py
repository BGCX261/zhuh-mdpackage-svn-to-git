
#from setuptools import setup
from distutils.core import setup
import sys

try:
    import numpy
except ImportError:
    print "*** package 'numpy' not found ***"
    print "Please get it from http://numpy.scipy.org/ or install it through your package manager."
    sys.exit(-1)



try:
    import MDAnalysis
except ImportError:
    print "*** package 'MDAnalysis' not found ***"
    sys.exit(-1)


setup(
        name='MDPackage',
        version='0.1.0',
        author="zhuh",
        packages=['MDPackage','MDPackage.data_analysis','MDPackage.mymath','MDPackage.Coor'],
        scripts=['scripts/Trjconv.py'\
                ,'scripts/Modify_Coor.py','scripts/entropy4gmx.py'\
                ,'scripts/Trj_info.py','scripts/Trj_modify.py','scripts/PDB_2_xtc.py','scripts/Hbond_occ.py'\
                ,'scripts/amber2xtc.py','scripts/LES_2_dcd.py','scripts/Read_Ambout.py'\
                ,'scripts/Rotate_2_Z.py','scripts/PW-rmsd.py']
        )

