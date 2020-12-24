# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\kryptic\generator\generator_test.py
# Compiled at: 2020-02-20 22:20:10
# Size of source mod 2**32: 351 bytes
import pytest
from .generator import Generator

@pytest.mark.parametrize('minlength,maxlength,minexpected,maxexpected', [(0, 0, 1, 1), (-1, 4, 1, 4), (5, -1, 5, 5), (10, 10, 10, 10)])
def test_getRandomLength(minlength, maxlength, minexpected, maxexpected):
    assert minexpected <= Generator(minlength, maxlength).getRandomLength(minlength, maxlength) >= maxexpected