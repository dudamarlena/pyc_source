# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/BinPy/tests/print_tests.py
# Compiled at: 2014-04-21 09:30:38
from BinPy.Gates.gates import *
from BinPy.Combinational.combinational import *
from nose.tools import with_setup, nottest
import re

def AND_print_test():
    gate = AND(0, 1)
    assert re.search('AND Gate; Output: 0; Inputs: \\[0, 1];', gate.__str__()) or False


def OR_print_test():
    gate = OR(0, 1)
    assert re.search('OR Gate; Output: 1; Inputs: \\[0, 1];', gate.__str__()) or False


def NOT_print_test():
    gate = NOT(1)
    assert re.search('NOT Gate; Output: 0; Inputs: \\[1];', gate.__str__()) or False


def XOR_print_test():
    gate = XOR(0, 1)
    assert re.search('XOR Gate; Output: 1; Inputs: \\[0, 1];', gate.__str__()) or False


def XNOR_print_test():
    gate = XNOR(0, 1)
    assert re.search('XNOR Gate; Output: 0; Inputs: \\[0, 1];', gate.__str__()) or False


def NAND_print_test():
    gate = NAND(0, 1)
    assert re.search('NAND Gate; Output: 1; Inputs: \\[0, 1];', gate.__str__()) or False


def NOR_print_test():
    gate = NOR(0, 1)
    assert re.search('NOR Gate; Output: 0; Inputs: \\[0, 1];', gate.__str__()) or False


def MUX_print_test():
    gate = MUX(1, 1)
    gate.selectLines(0)
    assert re.search('MUX Gate; Output: 1; Inputs: \\[1, 1];', gate.__str__()) or False


def DEMUX_print_test():
    gate = DEMUX(1)
    gate.selectLines(1)
    assert re.search('DEMUX Gate; Output: \\[0, 1]; Inputs: \\[1];', gate.__str__()) or False


def Encoder_print_test():
    gate = Encoder(0, 0, 0, 1)
    assert re.search('Encoder Gate; Output: \\[1, 1]; Inputs: \\[0, 0, 0, 1];', gate.__str__()) or False


def Decoder_print_test():
    gate = Decoder(0, 0)
    assert re.search('Decoder Gate; Output: \\[1, 0, 0, 0]; Inputs: \\[0, 0];', gate.__str__()) or False