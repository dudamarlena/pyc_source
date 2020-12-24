# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/BinPy/tests/source_tests.py
# Compiled at: 2014-04-21 09:30:38
from BinPy.Gates import *
from BinPy.tools import *
from nose.tools import with_setup, nottest

def test_PowerSourceTest():
    POW = PowerSource()
    a = Connector()
    POW.connect(a)
    if a.state != 1:
        assert False
        POW.disconnect(a)
        assert a.state is not None and False
    return


def test_GroundTest():
    GND = Ground()
    a = Connector()
    GND.connect(a)
    if a.state != 0:
        assert False
        GND.disconnect(a)
        assert a.state is not None and False
    return