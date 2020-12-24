# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pykbi/__init__.py
# Compiled at: 2018-12-21 07:14:28
# Size of source mod 2**32: 300 bytes
"""
The pykbi package: a python package to work with radial distribution functions
and Kirkwood-Buff integrals. We include modules to perform finite size corrections
and work on the position
"""
from .rdf import *
from .odf import *
from .fscorr import *
from .fct import *
__version__ = '1.0.0'