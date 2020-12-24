# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/lesson/arith2.py
# Compiled at: 2019-01-15 18:19:35
# Size of source mod 2**32: 1702 bytes
import string

def number(pos, data):
    rest = []
    while data[pos] and data[pos] in string.digits:
        rest.append(data[pos])
        pos += 1

    return (
     pos, int(''.join(rest)))


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
    rest = []
    while data[pos] and data[pos] in '*/':
        op = data[pos]
        pos, right = factor(pos + 1, data)
        rest.append([op, right])

    for op, right in rest:
        if op == '*':
            left *= right
        else:
            left /= right

    return (
     pos, left)


def expr(pos, data):
    pos, left = term(pos, data)
    rest = []
    while data[pos] and data[pos] in '+-':
        op = data[pos]
        pos, right = term(pos + 1, data)
        rest.append([op, right])

    for op, right in rest:
        if op == '+':
            left += right
        else:
            left -= right

    return (
     pos, left)


def evaluate(data):
    data = list(data)
    data.append(None)
    return expr(0, data)[1]