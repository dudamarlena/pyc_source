# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Equation\util.py
# Compiled at: 2014-07-06 22:44:47
try:
    from Equation import core
except ImportError:
    import core

def addFn(id, str, latex, args, func):
    core.functions[id] = {'str': str, 
       'latex': latex, 
       'args': args, 
       'func': func}


def addOp(id, str, latex, single, prec, func):
    if single:
        raise RuntimeError('Single Ops Not Yet Supported')
    core.ops[id] = {'str': str, 'latex': latex, 
       'args': 2, 
       'prec': prec, 
       'func': func}


def addUnaryOp(id, str, latex, func):
    core.unary_ops[id] = {'str': str, 
       'latex': latex, 
       'args': 1, 
       'prec': 0, 
       'func': func}


def addConst(name, value):
    core.constants[name] = value