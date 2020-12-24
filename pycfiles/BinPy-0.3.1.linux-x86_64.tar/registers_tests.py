# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/BinPy/tests/registers_tests.py
# Compiled at: 2014-04-21 09:30:38
from BinPy import *
from nose.tools import with_setup, nottest

def test_FourBitRegister():
    clock = Clock(1, 500)
    clock.start()
    test_ffr = FourBitRegister(1, 0, 1, 0, clock, 1)
    assert test_ffr.output() == [1, 0, 1, 0]
    clock.kill()


def test_FourBitLoadRegister():
    clock = Clock(1, 500)
    clock.start()
    test_ffr = FourBitLoadRegister(1, 0, 1, 0, clock, 1, 1)
    assert test_ffr.output() == [1, 0, 1, 0]
    test_ffr.setLoad(0)
    assert test_ffr.output() == [1, 0, 1, 0]
    clock.kill()


def test_ShiftRegister():
    clock = Clock(1, 500)
    clock.start()
    test_ffr = ShiftRegister([1, 0, 0, 0], clock)
    assert test_ffr.output() == [1, 1, 0, 0]
    assert test_ffr.output() == [1, 1, 1, 0]
    assert test_ffr.output() == [1, 1, 1, 1]
    test_ffr = ShiftRegister([1, 0, 0, 0], clock, circular=1)
    assert test_ffr.output() == [0, 1, 0, 0]
    assert test_ffr.output() == [0, 0, 1, 0]
    assert test_ffr.output() == [0, 0, 0, 1]
    clock.kill()