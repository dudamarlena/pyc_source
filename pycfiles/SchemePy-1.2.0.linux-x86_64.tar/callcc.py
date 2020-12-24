# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/callcc.py
# Compiled at: 2015-09-07 01:28:18
from zope.interface import implements, providedBy
from scheme.macro import Macro
from scheme.procedure import Procedure
from scheme.processer import Globals, processer as p
from scheme.utils import callCCBounce
from scheme.symbol import Symbol

class CCC(Symbol):

    def isBound(self, *args):
        return True

    def getEnv(self, *args):
        return Globals.Globals

    def toObject(self, *args):
        return callcc()


class callcc(object):
    implements(Procedure)

    def __init__(self):
        self.env = Globals.Globals

    def __call__(self, *args):
        if len(args) == 1:
            ast = args[0]
            processer = p
        else:
            processer, ast = args
        continuation = processer.continuation
        continuation['initialCallDepth'] += 1
        continuation['targetCallDepth'] = processer.callDepth
        callback = callccCallback(continuation, self)
        if Procedure in providedBy(ast[0]):
            processer.pushStack([[ast[0], callback]])
            r = processer.process([[ast[0], callback]], processer.cenv)
        elif Macro in providedBy(ast[0]):
            r = ast[0](processer, [callback])
            processer.pushStack(r)
            r = processer.process(r, processer.cenv)
            processer.popStack(r)
        else:
            r = ast[0](callback)
        return r


class callccCallback:
    implements(Procedure)

    def __init__(self, continuation, ccc):
        self.env = Globals
        self.continuation = continuation
        self.ccc = ccc

    def __call__(self, *args):
        if len(args) == 1:
            ast = args
            processer = p
        else:
            processer, ast = args
        processer.dumpStack()
        e = callCCBounce()
        e.continuation = self.continuation
        e.retval = ast[0]
        e.ccc = self.ccc
        raise e


Globals.Globals['call/cc'] = CCC('call/cc')