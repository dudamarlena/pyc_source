# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_units.py
# Compiled at: 2019-05-16 14:28:36
# Size of source mod 2**32: 643 bytes
"""
Run tests for the units module of vmlib
"""
import pytest
from pygeo2x import temp as _temp

def test_convert_temperature():
    assert _temp.convert_temperature(0, 'c', 'f') == 32
    assert _temp.convert_temperature(0, 'c', 'k') == 273.15
    assert _temp.convert_temperature(32, 'f', 'c') == 0
    assert _temp.convert_temperature(273.15, 'k', 'f') == 32
    assert _temp.convert_temperature(273.15, 'k', 'c') == 0
    with pytest.raises(AttributeError):
        _temp.convert_temperature(0, 'b', 'f')
    with pytest.raises(AttributeError):
        _temp.convert_temperature(0, 'c', 'b')