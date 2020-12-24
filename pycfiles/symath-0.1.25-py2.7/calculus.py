# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/symath/calculus.py
# Compiled at: 2015-08-21 11:58:24
from core import WildResults, wilds, symbolic, symbols
from functions import *
from stdops import *
from memoize import Memoize
_known_functions = (Log, Add, Sub, Mul, Div, Pow, Sin, Cos, Tan, Exp, Sum)

class DifferentiationError(Exception):
    pass


def _diff_known_function(expression, variable):
    vals = WildResults()
    g, h = wilds('g h')
    if expression[0] not in _known_functions:
        raise DifferentiationError('d/d%s  %s' % (variable, expression))
    if expression.match(g + h, vals):
        return diff(vals.g, variable) + diff(vals.h, variable)
    if expression.match(g - h, vals):
        return diff(vals.g, variable) - diff(vals.h, variable)
    if expression.match(variable ** g, vals):
        return vals.g * variable ** (vals.g - 1)
    if expression.match(g * h, vals):
        return vals.g * diff(vals.h, variable) + vals.h * diff(vals.g, variable)
    if expression.match(g / h, vals):
        return (diff(vals.g, variable) * vals.h - vals.g * diff(vals.h, variable)) / vals.h ** 2
    if expression.match(Exp(variable)):
        return expression
    if expression.match(Sin(variable)):
        return Sin(variable)
    if expression.match(Cos(variable)):
        return -1 * Sin(variable)
    if expression.match(Sum(g, h), vals):
        if variable(vals.g) in vals.h:
            return Sum(vals.g, diff(vals.h, variable(vals.g)))
        else:
            return Sum(vals.g, diff(vals.h, variable))

    elif expression.match(Log(variable), vals):
        return 1.0 / variable
    raise DifferentiationError('d/d%s  %s' % (variable, expression))


def diff(expression, variable):
    vals = WildResults()
    f, a, b = wilds('f a b')
    expression = expression.simplify()
    if variable not in expression:
        return symbolic(0)
    if expression.match(variable):
        return symbolic(1)
    if expression.match(f(a, b), vals) and vals.f in _known_functions:
        return _diff_known_function(expression, variable)
    if expression.match(f(a), vals) and vals.f in _known_functions:
        return _diff_known_function(vals.f(vals.a), vals.a) * diff(vals.a, variable)
    raise DifferentiationError('d/d%s  %s' % (variable, expression))