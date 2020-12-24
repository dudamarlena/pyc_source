# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pmx/__init__.py
# Compiled at: 2019-03-19 12:07:40
__doc__ = '\npmx is a collection of classes and functions to deal with\nmolecular structure files. It makes use of some functions\nfrom the GROMACS molecular dynamics package to read and write\nstructure files, e.g. trajectory data, but also to allow fast\nneighborsearching from a python script.\nQuite fancy is the interface to the GROMACS command line parsing\nfunctionality. Take a look at the example scripts.\n\n'
import os
from atom import *
from molecule import *
from chain import *
from model import *
from options import *
XX = 0
YY = 1
ZZ = 2
from ._version import get_versions
__version__ = get_versions()['version']
PMX_VERSION = __version__
del get_versions