# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/lesson/arith5.py
# Compiled at: 2019-01-15 21:45:27
# Size of source mod 2**32: 2730 bytes
import string

def oper(args):
    left, rest = args
    for op, right in rest:
        if op == '*':
            left *= right
        else:
            if op == '/':
                left /= right
            else:
                if op == '+':
                    left += right
                else:
                    left -= right

    return left


def number(pos, data):
    digits = many(inset(string.digits))
    p = _map(digits, lambda x: int(''.join(x)))
    return p(pos, data)


def factor(pos, data):
    subexpr = _map(seq(char('('), expr, char(')')), lambda x: x[1])
    p = choice(subexpr, number)
    return p(pos, data)


def term(pos, data):
    p = _map(seq(factor, many(seq(inset('*/'), factor))), oper)
    return p(pos, data)


def expr(pos, data):
    p = _map(seq(term, many(seq(inset('+-'), term))), oper)
    return p(pos, data)


def evaluate(data):
    data = list(data)
    data.append(None)
    return expr(0, data)[1]


def char(c):

    def process(pos, data):
        if data[pos] == c:
            return (
             pos + 1, c)
        raise Exception()

    return process


def inset(s):

    def process(pos, data):
        v = set(s)
        if data[pos] in v:
            return (
             pos + 1, data[pos])
        raise Exception()

    return process


def many(p):

    def process(pos, data):
        rest = []
        while True:
            try:
                pos, r = p(pos, data)
                rest.append(r)
            except Exception:
                break

        return (
         pos, rest)

    return process


def seq(*args):

    def process(pos, data):
        rest = []
        for p in args:
            pos, r = p(pos, data)
            rest.append(r)

        return (
         pos, rest)

    return process


def choice(*args):

    def process(pos, data):
        e = None
        for p in args:
            try:
                return p(pos, data)
            except Exception as ex:
                e = ex

        raise e

    return process


def _map(p, func):

    def process(pos, data):
        pos, res = p(pos, data)
        return (pos, func(res))

    return process