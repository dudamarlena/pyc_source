# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/io.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1075 bytes
"""
Input/Output module

.. warning:: This module has been deprecated and will be removed in the future.

        All spm1d procedures accept NumPy arrays directly, and NumPy load/save
        functionality has greatly improved in the last few years, so spm1d-specific
        data IO has been made redundant. Consider using the following functions:
        
        * numpy.loadtxt
        * numpy.savetxt
        * numpy.load
        * numpy.save
        * scipy.io.loadmat
        * scipy.io.savemat
"""

class Deprecated(object):

    def __init__(self, f):
        fnname = 'spm1d.io.' + f.__name__
        self.msg = '"%s" has been deprecated.  The "spm1d.io" module will be removed in the future.' % fnname

    def __call__(self, *args):
        raise DeprecationWarning(self.msg)


@Deprecated
def load(*args):
    pass


@Deprecated
def loadmat(*args):
    pass


@Deprecated
def loadspm(*args):
    pass


@Deprecated
def loadtxt(*args):
    pass


@Deprecated
def save(*args):
    pass


@Deprecated
def savemat(*args):
    pass


@Deprecated
def savespm(*args):
    pass


@Deprecated
def savetxt(*args):
    pass