# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/symath/isymath.py
# Compiled at: 2015-08-21 11:58:24
from symath import symbols, wilds, WildResults, functions, stdops
from IPython.display import Latex
_greek = symbols('theta gamma Theta Gamma alpha beta Alpha Beta Delta delta pi Pi phi Phi')

def _idisplay(exp):
    x, y, z, n = wilds('x y z n')
    ws = WildResults()
    if exp.match(x ** y, ws):
        return '{%s} ^  {%s}' % (_idisplay(ws.x), _idisplay(ws.y))
    else:
        if exp in _greek:
            return '\\%s' % (str(exp),)
        if exp.match(-1 * x, ws):
            return '-{%s}' % (_idisplay(ws.x),)
        if exp.match(x + y, ws):
            return '{%s} + {%s}' % (_idisplay(ws.x), _idisplay(ws.y))
        if exp.match(x - y, ws):
            return '{%s} - {%s}' % (_idisplay(ws.x), _idisplay(ws.y))
        if exp.match(x * y, ws):
            return '{%s} {%s}' % (_idisplay(ws.x), _idisplay(ws.y))
        if exp.match(x / y, ws):
            return '\\frac{%s}{%s}' % (_idisplay(ws.x), _idisplay(ws.y))
        if exp.match(x ^ y, ws):
            return '{%s}  \\oplus  {%s}' % (_idisplay(ws.x), _idisplay(ws.y))
        if exp.match(functions.Exp(x), ws):
            return 'e^{%s}' % (_idisplay(ws.x),)
        if exp.match(x(y), ws) and ws.x in [
         functions.ArcCos, functions.ArcSin,
         functions.ArcTan, functions.Cos,
         functions.Sin, functions.Tan]:
            return '\\%s{%s}' % (str(ws.x).lower(), _idisplay(ws.y))
        if exp.match(stdops.Equal(x, y), ws):
            return '%s = %s' % (_idisplay(ws.x), _idisplay(ws.y))
        if exp.match(functions.Sum(n, x), ws):
            return '\\sum_{%s}{%s}' % (_idisplay(ws.n), _idisplay(ws.x))
        return str(exp)


def idisplay(exp):
    return Latex('$' + _idisplay(exp) + '$')


a, b, c, j, theta, e, alpha = symbols('a b c j theta e alpha')
idisplay(stdops.Equal(functions.Exp(j * theta) / alpha, (functions.Cos(theta) + j * functions.Sin(theta)) / alpha))