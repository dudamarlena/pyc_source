# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/let.py
# Compiled at: 2015-09-04 17:30:49
from scheme.debug import LOG
from scheme.environment import Environment
from scheme.procedure import SimpleProcedure
__author__ = 'perkins'
from scheme.macro import Macro
from scheme.Globals import Globals
from zope.interface import implements

class let(object):
    implements(Macro)

    def __init__(self):
        pass

    def __call__(self, processer, params):
        env = processer.cenv
        print 18, env
        if isinstance(params[0], list):
            bindings = params[0]
            e = Environment(env)
            for binding in bindings:
                if len(binding[1:]) != 1:
                    raise SyntaxError('let requires a list of pairs for its first argument')
                if isinstance(binding[1], list):
                    b = binding[1]
                else:
                    b = binding[1]
                processer.pushStack(b)
                r = processer.process(b, Environment(env), processer.initialCallDepth)
                processer.popStack(r)
                e[binding[0]] = r

            r = processer.process(params[1:], e, processer.callDepth)
            processer.popStack(r)
            processer.popStack(r)
            return
        name = params[0]
        bindings = params[1]
        vars_ = [ i[0] for i in bindings ]
        vals = [ processer.process(i[1], Environment(env)) for i in bindings ]
        proc = SimpleProcedure([vars_] + params[2:], env).setName(name)
        env[name] = proc
        LOG('LET', 32, [proc] + vals)
        ret = processer.process([[proc] + vals])
        processer.popStack(ret)
        processer.stackPointer += 1


Globals['let'] = let()