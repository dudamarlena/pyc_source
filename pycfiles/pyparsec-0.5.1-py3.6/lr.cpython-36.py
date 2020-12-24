# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/test/lr.py
# Compiled at: 2015-12-14 04:46:07
# Size of source mod 2**32: 1108 bytes
from parsec import *
import string
input = '1*2+3*(4+5)'
digit = oneOf(string.digits)

@Parsec
def integer(st):
    re = many1(digit)(st)
    return int(''.join(re))


def mulN(x):

    @Parsec
    def func(st):
        y = eq('*').then(N)(st)
        return x * y

    return func


def addF(x):

    @Parsec
    def func(st):
        y = eq('+').then(F)(st)
        return x + y

    return func


@Parsec
def N(st):
    return choice(attempt(integer), between(eq('('), eq(')'), T))(st)


@Parsec
def F(st):
    return choice(attempt(N), F).bind(mulN)(st)


@Parsec
def T(st):
    return choice(attempt(F), T).bind(addF)(st)


if __name__ == '__main__':
    st = BasicState(input)
    re = T(st)
    print(re)