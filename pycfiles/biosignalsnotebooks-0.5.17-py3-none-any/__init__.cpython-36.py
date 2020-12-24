# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\gui_s\AppData\Local\Temp\pip-build-vljg4uzq\pyedflib\pyedflib\__init__.py
# Compiled at: 2018-06-15 05:54:11
# Size of source mod 2**32: 735 bytes
from __future__ import division, print_function, absolute_import
from ._extensions._pyedflib import *
from .edfwriter import *
from .edfreader import *
from . import data
from pyedflib.version import version as __version__
from numpy.testing import Tester
__all__ = [s for s in dir() if not s.startswith('_')]
try:
    del s
except NameError:
    pass

test = Tester().test