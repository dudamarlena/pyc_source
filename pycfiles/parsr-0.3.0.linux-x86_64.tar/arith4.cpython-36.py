# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/lesson/arith4.py
# Compiled at: 2019-01-15 18:19:35
# Size of source mod 2**32: 1969 bytes
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
    pos, res = many(pos, data, string.digits)
    return (
     pos, int(''.join(res)))


def factor(pos, data):
    if data[pos] == '(':
        pos, res = expr(pos + 1, data)
        assert data[pos] == ')', 'Unmatched paren.'
        return (
         pos + 1, res)
    else:
        return number(pos, data)


def term(pos, data):
    pos, left = factor(pos, data)
    pos, rest = many(pos, data, '*/', factor)
    return (
     pos, oper([left, rest]))


def expr(pos, data):
    pos, left = term(pos, data)
    pos, rest = many(pos, data, '+-', term)
    return (
     pos, oper([left, rest]))


def evaluate(data):
    data = list(data)
    data.append(None)
    return expr(0, data)[1]


def many(pos, data, cs, rhs=None):
    rest = []
    while data[pos] and data[pos] in cs:
        op = data[pos]
        if rhs:
            pos, right = rhs(pos + 1, data)
            rest.append([op, right])
        else:
            rest.append(op)
            pos += 1

    return (
     pos, rest)