# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsr/examples/arith.py
# Compiled at: 2019-11-14 13:57:46
"""
Simple arithmetic with usual operator precedence and associativity. It allows
addition, subtraction, multiplication, division, and grouping with parentheses.
"""
from insights.parsr import EOF, Forward, InSet, LeftParen, Many, Number, RightParen, WS

def evaluate(e):
    return Top(e)[0]


def op(args):
    ans, rest = args
    for op, arg in rest:
        if op == '+':
            ans += arg
        elif op == '-':
            ans -= arg
        elif op == '*':
            ans *= arg
        elif op == '/':
            ans /= arg

    return ans


HighOps = InSet('*/')
LowOps = InSet('+-')
expr = Forward() % 'expr forward'
factor = WS >> (Number % 'Number' | LeftParen >> expr << RightParen) << WS
term = (factor + Many(HighOps + factor)).map(op) % 'term'
expr <= (term + Many(LowOps + term)).map(op) % 'expr'
Top = (expr + EOF) % 'Top'