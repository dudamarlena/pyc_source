# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/BinPy/tests/analog_source_tests.py
# Compiled at: 2014-04-21 09:30:38
from BinPy.Analog import *
from nose.tools import with_setup, nottest

def test_SinWaveVoltageSource():
    source = SinWaveVoltageSource()
    assert source.getParams()['e'] == 0
    assert source.getParams()['t'] == 0
    assert source.getParams()['w'] == 0
    assert source.getParams()['V'] == 0
    assert source.getParams()['H'].state == 0.0
    assert source.getParams()['L'].state == 0
    params = {'V': 5, 'w': 10, 't': 10, 'e': 0}
    source.setParams(params)
    assert source.getParams()['e'] == 0
    assert source.getParams()['t'] == 10
    assert source.getParams()['w'] == 10
    assert source.getParams()['V'] == 5
    assert source.getParams()['H'].state == 4.9
    assert source.getParams()['L'].state == 0
    params = {'V': 5, 'w': 0, 't': 0, 'e': 90}
    source.setParams(params)
    assert source.getParams()['e'] == 90
    assert source.getParams()['t'] == 0
    assert source.getParams()['w'] == 0
    assert source.getParams()['V'] == 5
    assert source.getParams()['H'].state == 5.0
    assert source.getParams()['L'].state == 0


def test_CosWaveVoltageSource():
    source = CosWaveVoltageSource()
    assert source.getParams()['e'] == 0
    assert source.getParams()['t'] == 0
    assert source.getParams()['w'] == 0
    assert source.getParams()['V'] == 0
    assert source.getParams()['H'].state == 0.0
    assert source.getParams()['L'].state == 0
    params = {'V': 5, 'w': 10, 't': 10, 'e': 0}
    source.setParams(params)
    assert source.getParams()['e'] == 0
    assert source.getParams()['t'] == 10
    assert source.getParams()['w'] == 10
    assert source.getParams()['V'] == 5
    assert source.getParams()['H'].state == -0.8500000000000001
    assert source.getParams()['L'].state == 0
    params = {'V': 5, 'w': 0, 't': 0, 'e': 90}
    source.setParams(params)
    assert source.getParams()['e'] == 90
    assert source.getParams()['t'] == 0
    assert source.getParams()['w'] == 0
    assert source.getParams()['V'] == 5
    assert source.getParams()['H'].state == 0.0
    assert source.getParams()['L'].state == 0


def test_SinWaveCurrentSource():
    source = SinWaveCurrentSource()
    assert source.getParams()['e'] == 0
    assert source.getParams()['t'] == 0
    assert source.getParams()['w'] == 0
    assert source.getParams()['I'] == 0
    assert source.getParams()['i'] == 0.0
    assert source.getParams()['H'].state == 0
    assert source.getParams()['L'].state == 0
    params = {'I': 5, 'w': 10, 't': 10, 'e': 0}
    source.setParams(params)
    assert source.getParams()['e'] == 0
    assert source.getParams()['t'] == 10
    assert source.getParams()['w'] == 10
    assert source.getParams()['I'] == 5
    assert source.getParams()['i'] == 4.9
    assert source.getParams()['H'].state == 0
    assert source.getParams()['L'].state == 0
    params = {'I': 5, 'w': 0, 't': 0, 'e': 90}
    source.setParams(params)
    assert source.getParams()['e'] == 90
    assert source.getParams()['t'] == 0
    assert source.getParams()['w'] == 0
    assert source.getParams()['I'] == 5
    assert source.getParams()['i'] == 5.0
    assert source.getParams()['H'].state == 0
    assert source.getParams()['L'].state == 0


def test_CosWaveCurrentSource():
    source = CosWaveCurrentSource()
    assert source.getParams()['e'] == 0
    assert source.getParams()['t'] == 0
    assert source.getParams()['w'] == 0
    assert source.getParams()['I'] == 0
    assert source.getParams()['i'] == 0.0
    assert source.getParams()['H'].state == 0
    assert source.getParams()['L'].state == 0
    params = {'I': 5, 'w': 10, 't': 10, 'e': 0}
    source.setParams(params)
    assert source.getParams()['e'] == 0
    assert source.getParams()['t'] == 10
    assert source.getParams()['w'] == 10
    assert source.getParams()['I'] == 5
    assert source.getParams()['i'] == -0.8500000000000001
    assert source.getParams()['H'].state == 0
    assert source.getParams()['L'].state == 0
    params = {'I': 5, 'w': 0, 't': 0, 'e': 90}
    source.setParams(params)
    assert source.getParams()['e'] == 90
    assert source.getParams()['t'] == 0
    assert source.getParams()['w'] == 0
    assert source.getParams()['I'] == 5
    assert source.getParams()['i'] == 0.0
    assert source.getParams()['H'].state == 0
    assert source.getParams()['L'].state == 0