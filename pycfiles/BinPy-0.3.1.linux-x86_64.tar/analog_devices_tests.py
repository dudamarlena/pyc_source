# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/BinPy/tests/analog_devices_tests.py
# Compiled at: 2014-04-21 09:30:38
from BinPy.Analog import *
from nose.tools import with_setup, nottest

def test_Resisitor():
    params = {'r': 5}
    r = Resistor(params)
    assert r.getParams()['i'] == 0
    assert r.getParams()['r'] == 5
    assert r.getParams()['+'].state == 0
    assert r.getParams()['-'].state == 0
    r.setVoltage(Connector(5), Connector(0))
    assert r.getParams()['i'] == 1.0
    assert r.getParams()['r'] == 5
    assert r.getParams()['+'].state == 5
    assert r.getParams()['-'].state == 0
    r.setCurrent(10)
    assert r.getParams()['i'] == 10
    assert r.getParams()['r'] == 5
    assert r.getParams()['+'].state == 50
    assert r.getParams()['-'].state == 0
    r.setResistance(10)
    assert r.getParams()['i'] == 5.0
    assert r.getParams()['r'] == 10
    assert r.getParams()['+'].state == 50
    assert r.getParams()['-'].state == 0