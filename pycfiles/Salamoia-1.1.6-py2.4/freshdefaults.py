# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/freshdefaults.py
# Compiled at: 2007-12-02 16:26:56
from copy import deepcopy

def freshdefaults(f):
    """wrap f and keep its default values fresh between calls"""
    fdefaults = f.func_defaults

    def refresher(*args, **kwds):
        f.func_defaults = deepcopy(fdefaults)
        return f(*args, **kwds)

    return refresher


from salamoia.tests import *
runDocTests()