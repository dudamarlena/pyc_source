# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hdf5_matlab_reader/__init__.py
# Compiled at: 2016-03-22 17:37:34
# Size of source mod 2**32: 127 bytes
__version__ = '0.1.2'
from .matlab_reader import loadmat
from .tree_printer import tree
from .empty_matrix import EmptyMatrix