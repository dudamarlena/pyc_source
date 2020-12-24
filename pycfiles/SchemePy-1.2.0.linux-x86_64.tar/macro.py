# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/macro.py
# Compiled at: 2015-09-07 05:20:32
from zope.interface import providedBy
from scheme.debug import LOG
from scheme.procedure import Procedure
from scheme.utils import copy_with_quasiquote, deepcopy
import scheme
__author__ = 'perkins'
from zope import interface
from scheme.symbol import Symbol
from scheme.environment import Environment
import scheme

class Macro(interface.Interface):

    def __init__(ast, env):
        """"""
        pass

    def __call__(processer, params):
        """"""
        pass


class MacroSymbol(Symbol):

    def getEnv(self, env):
        if hasattr(self, 'env'):
            return self.env
        raise NameError('MacroSymbol has no associated environment')

    def setObj(self, obj):
        self.obj = obj
        return self

    def toObject(self, env):
        if hasattr(self, 'obj'):
            return self.obj
        else:
            e = env
            while e is not None:
                if e is self.env:
                    return Symbol.toObject(self, env)
                if hasattr(e, 'parent'):
                    e = e.parent
                else:
                    e = None

            return Symbol.toObject(self, self.env)

    def setEnv(self, env):
        self.env = Environment(env)
        if not hasattr(self.env.parent, 'parent'):
            self.env.parent = Environment(scheme.Globals.Globals, env)
        return self

    def __call__(self, *args):
        from jit import isaProcedure
        f = self.toObject({})
        if args and isinstance(args[0], scheme.processer.Processer):
            processer, ast = args
        else:
            processer = scheme.processer.current_processer
            ast = list(args)
        if isaProcedure(f):
            return f(processer, ast)
        return f(*ast)


class SimpleMacro(object):
    interface.implements(Macro)

    @classmethod
    def wrappedMacro(cls, proc, env):
        while isinstance(proc, Symbol):
            proc = proc.toObject(env)

        pb = providedBy(proc)
        if Macro in pb:
            return proc
        else:
            if Procedure in pb:
                return cls(None, env, proc).setName(proc.name)
            return cls(None, env, proc)

    def __init__(self, ast, env, wrapped=None):
        self.ast = ast
        self.env = env
        self.name = None
        self.wrapped = wrapped
        return

    def __call__(self, processer, args):
        if self.wrapped:
            if Procedure in providedBy(self.wrapped):
                return self.wrapped(processer, args)
            return self.wrapped(args)
        else:
            retval = None
            env = Environment(self.env)
            if isinstance(self.ast[0], list):
                if '.' in self.ast[0]:
                    idx = -1
                    item = None
                    for idx, item in enumerate(self.ast[0][:-2]):
                        i = args[idx]
                        env[item] = i

                    env[self.ast[0][(-1)]] = args[idx + 1:]
                else:
                    if len(self.ast[0]) != len(args):
                        raise SyntaxError('Macro %r requires exactly %i args, %i given' % (self, len(self.ast[0]), len(args)))
                    for idx, item in enumerate(self.ast[0]):
                        i = args[idx]
                        env[item] = i

            else:
                env[self.ast[0]] = [
                 Symbol('quote'), args]
            o = []
            retval = copy_with_quasiquote(processer, env, deepcopy(self.ast[1:]), o_stack=o)[0]
            LOG('macro', retval)
            retval = processer.process(retval, processer.cenv)
            processer.popStack(retval)
            return

    def setName(self, name):
        self.name = name
        return self

    def __repr__(self):
        if self.name:
            return '<SimpleMacro %s>' % self.name
        return object.__repr__(self)