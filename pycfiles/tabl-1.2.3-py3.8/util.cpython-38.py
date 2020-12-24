# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/tabl/util.py
# Compiled at: 2020-03-12 15:31:38
# Size of source mod 2**32: 802 bytes
"""
.. module:: tabl.util
.. moduleauthor:: Bastiaan Bergman <Bastiaan.Bergman@gmail.com>

"""
from __future__ import absolute_import, division, print_function, unicode_literals
import sys
if sys.version_info >= (3, 0):
    PV = 3
    ImpError = ModuleNotFoundError
else:
    if sys.version_info >= (2, 0):
        PV = 2
        ImpError = ImportError
    else:
        print('Forget about it!')
        sys.exit(1)

def isstring(strng):
    """ Python version independent string checking """
    if PV == 2:
        return isinstance(strng, basestring)
    if PV == 3:
        return isinstance(strng, str)
    raise NotImplementedError('Unknown python verison: {}'.format(PV))