# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/gplearn/translateFn.py
# Compiled at: 2020-05-13 00:13:20
# Size of source mod 2**32: 3476 bytes


def abs(a):
    return 'abs(' + str(a) + ')'


def cbrt(a):
    return 'cbrt(' + str(a) + ')'


def hypot(a, b):
    return 'hypot(' + str(a) + ',' + str(b) + ')'


def sigmoid(a):
    return 'sigmoid(' + str(a) + ')'


def ceil(a):
    return 'ceil(' + str(a) + ')'


def fabs(a):
    return 'fabs(' + str(a) + ')'


def floor(a):
    return 'floor(' + str(a) + ')'


def trunc(a):
    return 'trunc(' + str(a) + ')'


def sub(a, b):
    return '(' + str(a) + '-' + str(b) + ')'


def add(a, b):
    return '(' + str(a) + '+' + str(b) + ')'


def mul(a, b):
    return '(' + str(a) + '*' + str(b) + ')'


def div(a, b):
    return '(' + str(a) + '/' + str(b) + ')'


def sqrt(a):
    return 'sqrt(' + str(a) + ')'


def log(a):
    return 'log(' + str(a) + ')'


def abs(a):
    return 'abs(' + str(a) + ')'


def neg(a):
    return 'neg(' + str(a) + ')'


def inv(a):
    return 'inv(' + str(a) + ')'


def max(a, b):
    return 'max(' + str(a) + ',' + str(b) + ')'


def min(a, b):
    return 'min(' + str(a) + ',' + str(b) + ')'


def sin(a):
    return 'sin(' + str(a) + ')'


def cos(a):
    return 'cos(' + str(a) + ')'


def tan(a):
    return 'tan(' + str(a) + ')'


def modulox(a, b):
    return 'modulox(' + str(a) + ',' + str(b) + ')'


def xor(a, b):
    return 'xor(' + str(a) + ',' + str(b) + ')'


def or_(a, b):
    return 'or(' + str(a) + ',' + str(b) + ')'


def and_(a, b):
    return 'and(' + str(a) + ',' + str(b) + ')'


def heaviside(a, b):
    return 'heaviside(' + str(a) + ',' + str(b) + ')'


def zegax(a, b):
    return 'zegax(' + str(a) + ',' + str(b) + ')'


def moyenne2(a, b):
    return 'mean(' + ','.join(map(str, [a, b])) + ')'


def moyenne3(a, b, c):
    return 'mean(' + ','.join(map(str, [a, b, c])) + ')'


def moyenne4(a, b, c, d):
    return 'mean(' + ','.join(map(str, [a, b, c, d])) + ')'


def moyenne5(a, b, c, d, e):
    return 'mean(' + ','.join(map(str, [a, b, c, d, e])) + ')'


def moyenne6(a, b, c, d, e, f):
    return 'mean(' + ','.join(map(str, [a, b, c, d, e, f])) + ')'


def moyenne7(a, b, c, d, e, f, g):
    return 'mean(' + ','.join(map(str, [a, b, c, d, e, f, g])) + ')'


def moyenne8(a, b, c, d, e, f, g, h):
    return 'mean(' + ','.join(map(str, [a, b, c, d, e, f, g, h])) + ')'


def moyenne9(a, b, c, d, e, f, g, h, j):
    return 'mean(' + ','.join(map(str, [a, b, c, d, e, f, g, h, j])) + ')'


def moyenne10(a, b, c, d, e, f, g, h, j, k):
    return 'mean(' + ','.join(map(str, [a, b, c, d, e, f, g, h, j, k])) + ')'


def moyenne(*argu):
    return 'mean(' + ','.join(map(str, argu)) + ')'


class translateFunctions:

    def __init__(self, funct, kwargs):
        for k, v in kwargs.items():
            exec(str(k) + '=0')
            exec(str(k) + '=' + str(v))

        exec('self.y=' + funct)

    def getter(self):
        return self.y