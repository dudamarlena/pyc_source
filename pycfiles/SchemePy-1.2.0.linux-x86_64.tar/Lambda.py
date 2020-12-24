# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/Lambda.py
# Compiled at: 2015-09-06 18:06:47
__author__ = 'perkins'
from zope.interface import implements
from scheme.macro import Macro, MacroSymbol
from scheme.procedure import SimpleProcedure
from processer import Globals
import time, scheme
from scheme import jit
lambdas = []

class Lambda(object):
    implements(Macro)

    def __init__(self):
        pass

    def __call__(self, *a):
        if len(a) == 1:
            processer = scheme.processer.processer
            params = a[0]
        else:
            processer, params = a
        args = params[0]
        rest = params[1:]
        t = repr(time.time())
        proc = SimpleProcedure([args] + rest, processer.cenv).setName('lambda:%s' % t)
        if jit.enabled and jit.lambdas_enabled:
            proc = jit.makeFunction(proc)
        ret = MacroSymbol('lambda:%s' % t).setEnv({'lambda:%s' % t: proc})
        return ret


Globals.Globals['lambda'] = Lambda()