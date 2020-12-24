# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/conftest.py
# Compiled at: 2020-03-04 21:41:25
# Size of source mod 2**32: 214 bytes
import pytest
from flipy.lp_variable import LpVariable

@pytest.fixture
def x():
    return LpVariable('x', low_bound=0, up_bound=10)


@pytest.fixture
def y():
    return LpVariable('y', low_bound=0, up_bound=5)