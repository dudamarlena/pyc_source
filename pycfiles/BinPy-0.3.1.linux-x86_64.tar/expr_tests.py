# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/BinPy/tests/expr_tests.py
# Compiled at: 2014-04-21 09:30:38
from BinPy import *
from nose.tools import with_setup, nottest

def parse_test():
    assert Expr('A & B').parse() == 'AND(B, A)'
    assert Expr('(A & B)').parse() == 'AND(B, A)'
    assert Expr('(~A) & B').parse() == 'AND(B, NOT(A))'
    assert Expr('~(A & B)').parse() == 'NAND(B, A)'
    assert Expr('A | B').parse() == 'OR(B, A)'
    assert Expr('A ^ B').parse() == 'XOR(B, A)'
    assert Expr('A ^ ~B').parse() == 'XOR(NOT(B), A)'