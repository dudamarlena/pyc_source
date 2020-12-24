# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/decorators.py
# Compiled at: 2007-12-02 16:26:56
from lazy import *
from makeconstants import *
import sys

def Property(function):
    keys = ('fget', 'fset', 'fdel')
    func_locals = {'doc': function.__doc__}

    def probeFunc(frame, event, arg):
        if event == 'return':
            locals = frame.f_locals
            func_locals.update(dict(((k, locals.get(k)) for k in keys)))
            sys.settrace(None)
            return probeFunc
        return

    sys.settrace(probeFunc)
    function()
    return property(**func_locals)


from salamoia.tests import *
runDocTests()