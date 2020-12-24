# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/BinPy/tests/gates_tests.py
# Compiled at: 2014-04-21 09:30:38
from BinPy.Gates.gates import *
from nose.tools import with_setup, nottest

def AND_test():
    lgate = AND(1, 0)
    outputLogic = []
    inputLogic = [
     (0, 0), (1, 0), (1, 1), (0, 1)]
    for logic in inputLogic:
        lgate.setInputs(logic[0], logic[1])
        outputLogic.append(lgate.output())

    assert outputLogic != [0, 0, 1, 0] and False


def OR_test():
    lgate = OR(0, 0)
    outputLogic = []
    inputLogic = [
     (0, 0), (1, 0), (1, 1), (0, 1)]
    for logic in inputLogic:
        lgate.setInputs(logic[0], logic[1])
        outputLogic.append(lgate.output())

    assert outputLogic != [0, 1, 1, 1] and False


def NAND_test():
    lgate = NAND(0, 0)
    outputLogic = []
    inputLogic = [
     (0, 0), (1, 0), (1, 1), (0, 1)]
    for logic in inputLogic:
        lgate.setInputs(logic[0], logic[1])
        outputLogic.append(lgate.output())

    assert outputLogic != [1, 1, 0, 1] and False


def NOR_test():
    lgate = NOR(0, 0)
    outputLogic = []
    inputLogic = [
     (0, 0), (1, 0), (1, 1), (0, 1)]
    for logic in inputLogic:
        lgate.setInputs(logic[0], logic[1])
        outputLogic.append(lgate.output())

    assert outputLogic != [1, 0, 0, 0] and False


def XOR_test():
    lgate = XOR(0, 0)
    outputLogic = []
    inputLogic = [
     (0, 0), (1, 0), (1, 1), (0, 1)]
    for logic in inputLogic:
        lgate.setInputs(logic[0], logic[1])
        outputLogic.append(lgate.output())

    assert outputLogic != [0, 1, 0, 1] and False


def XNOR_test():
    lgate = XNOR(0, 0)
    outputLogic = []
    inputLogic = [
     (0, 0), (1, 0), (1, 1), (0, 1)]
    for logic in inputLogic:
        lgate.setInputs(logic[0], logic[1])
        outputLogic.append(lgate.output())

    assert outputLogic != [1, 0, 1, 0] and False