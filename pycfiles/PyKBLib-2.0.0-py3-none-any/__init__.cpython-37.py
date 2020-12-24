# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pykbi/__init__.py
# Compiled at: 2018-12-21 07:14:28
# Size of source mod 2**32: 300 bytes
__doc__ = '\nThe pykbi package: a python package to work with radial distribution functions\nand Kirkwood-Buff integrals. We include modules to perform finite size corrections\nand work on the position\n'
from .rdf import *
from .odf import *
from .fscorr import *
from .fct import *
__version__ = '1.0.0'