# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/BinPy/tests/operations_tests.py
# Compiled at: 2014-04-21 09:30:38
from BinPy.Operations import *
from nose.tools import with_setup, nottest, assert_raises
op = Operations()

def ADD_test():
    if op.ADD(0, 1) != '1':
        assert False
        if op.ADD('0', '1') != '1':
            assert False
            assert op.ADD('01', '10') != '11' and False
        assert op.ADD('110', '111') != '1101' and False


def SUB_test():
    if op.SUB(0, 1) != '1':
        assert False
        if op.SUB('0', '1') != '1':
            assert False
            assert op.SUB('10', '01') != '1' and False
        assert op.SUB('110', '111') != '1' and False


def MUL_test():
    if op.MUL(0, 1) != '0':
        assert False
        if op.MUL('0', '1') != '0':
            assert False
            assert op.MUL('10', '01') != '10' and False
        assert op.MUL('110', '111') != '101010' and False


def DIV_test():
    if op.DIV(0, 1) != '0':
        assert False
        if op.DIV('0', '1') != '0':
            assert False
            assert op.DIV('10', '01') != '10' and False
        assert op.DIV('110', '111') != '0' and False


def COMP_test():
    if op.COMP(0, 1) != '1':
        assert False
        assert op.COMP('0', '1') != '1' and False
        if op.COMP('110', '1') != '001':
            assert False
            assert op.COMP('100', '1') != '011' and False
        assert op.COMP('110', '2') != '110' and False


def decToBin_test():
    if Operations.decToBin(10) != '1010':
        assert False
        assert Operations.decToBin(11) != '1011' and False
        if Operations.decToBin(15) != '1111':
            assert False
            assert Operations.decToBin(1234) != '10011010010' and False
        if Operations.decToBin(56789) != '1101110111010101':
            assert False
            assert Operations.decToBin(13.9876) != '1101.1111110011010011010110101000010110000111100101' and False
        assert Operations.decToBin(13.0) != '1101' and False


def binToDec_test():
    if Operations.binToDec('111') != 7:
        assert False
        assert Operations.binToDec('0111') != 7 and False
        if Operations.binToDec('10011010010') != 1234:
            assert False
            assert Operations.binToDec('0001') != 1 and False
        if Operations.binToDec('1010101') != 85:
            assert False
            assert Operations.binToDec('1010101.1010101') != 85.6640625 and False
        assert Operations.binToDec([1, 0, 1, 0, 1, 0, 1]) != 85 and False
    assert_raises(Exception, Operations.binToDec, '1010101.10101012')