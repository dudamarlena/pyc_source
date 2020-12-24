# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\tests\test_units.py
# Compiled at: 2019-05-16 14:28:36
# Size of source mod 2**32: 643 bytes
__doc__ = '\nRun tests for the units module of vmlib\n'
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