# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pmx/__init__.py
# Compiled at: 2019-03-19 12:07:40
"""
pmx is a collection of classes and functions to deal with
molecular structure files. It makes use of some functions
from the GROMACS molecular dynamics package to read and write
structure files, e.g. trajectory data, but also to allow fast
neighborsearching from a python script.
Quite fancy is the interface to the GROMACS command line parsing
functionality. Take a look at the example scripts.

"""
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