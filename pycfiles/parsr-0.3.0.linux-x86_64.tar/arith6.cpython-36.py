# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/lesson/arith6.py
# Compiled at: 2019-01-16 11:00:38
# Size of source mod 2**32: 3452 bytes
import string

class Parser:

    def __add__(self, other):
        return Seq(self, other)

    def __or__(self, other):
        return Choice(self, other)

    def map(self, func):
        return Map(self, func)

    def __call__(self, data):
        data = list(data)
        data.append(None)
        return self.process(0, data)[1]


class Char(Parser):

    def __init__(self, c):
        self.c = c

    def process(self, pos, data):
        if data[pos] == self.c:
            return (
             pos + 1, self.c)
        raise Exception()


class InSet(Parser):

    def __init__(self, s):
        self.v = set(s)

    def process(self, pos, data):
        if data[pos] in self.v:
            return (
             pos + 1, data[pos])
        raise Exception()


class Many(Parser):

    def __init__(self, p):
        self.p = p

    def process(self, pos, data):
        rest = []
        while True:
            try:
                pos, r = self.p.process(pos, data)
                rest.append(r)
            except Exception:
                break

        return (
         pos, rest)


class Seq(Parser):

    def __init__(self, *args):
        self.args = list(args)

    def __add__(self, other):
        self.args.append(other)
        return self

    def process(self, pos, data):
        rest = []
        for p in self.args:
            pos, r = p.process(pos, data)
            rest.append(r)

        return (
         pos, rest)


class Choice(Parser):

    def __init__(self, *args):
        self.args = list(args)

    def __or__(self, other):
        self.args.append(other)
        return self

    def process(self, pos, data):
        e = None
        for p in self.args:
            try:
                return p.process(pos, data)
            except Exception as ex:
                e = ex

        raise e


class Map(Parser):

    def __init__(self, p, func):
        self.p = p
        self.func = func

    def process(self, pos, data):
        pos, res = self.p.process(pos, data)
        return (pos, self.func(res))


class Forward(Parser):

    def __init__(self):
        self.p = None

    def __le__(self, other):
        self.p = other

    def process(self, pos, data):
        return self.p.process(pos, data)


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


expr = Forward()
number = Many(InSet(string.digits)).map(lambda x: int(''.join(x)))
factor = (Char('(') + expr + Char(')')).map(lambda x: x[1]) | number
term = (factor + Many(InSet('*/') + factor)).map(oper)
expr <= (term + Many(InSet('+-') + term)).map(oper)

def evaluate(data):
    return expr(data)