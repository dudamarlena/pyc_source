# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/__init__.py
# Compiled at: 2019-02-16 12:05:51
# Size of source mod 2**32: 1236 bytes
"""
It's a Protein Data Bank (.pdb) files manipulation package that is
mainly developed to parse and load, duplicate, manipulate and create pdb files.
A full description of a pdb file can be found here: http://deposit.rcsb.org/adit/docs/pdb_atom_format.html
pdbparser atoms configuration can be visualized by vmd software (http://www.ks.uiuc.edu/Research/vmd/)
by simply pointing 'VMD_PATH' global variable to the exact path of vmd executable, and using 'visualize' method.
At any time and stage of data manipulation, a pdb file of all atoms or a subset of atoms can be exported to a pdb file.

Additional sub-modules (pdbTrajectory, etc) and sub-packages (Analysis, etc)
started to add up to pdbparser package, especially when traditional molecular dynamics data analysis softwares
couldn't keep up the good performance, feasibility and speed of calculation with the increasing
number of atoms in the simulated system.
"""
from __future__ import print_function
from .__pkginfo__ import __version__, __author__
from .pdbparser import pdbparser, pdbTrajectory