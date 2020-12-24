# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/test_lp_objective.py
# Compiled at: 2020-03-04 21:41:25
# Size of source mod 2**32: 916 bytes
import pytest
from flipy.lp_objective import LpObjective, Minimize, Maximize

@pytest.fixture
def objective(name='', expression=None, constant=0):
    return LpObjective(name, expression, constant)


class TestLpExpression(object):

    def test_init(self):
        obj = LpObjective(name='', expression=None, constant=0)
        assert obj
        assert obj.sense == Minimize
        obj.sense = Maximize
        assert obj.sense == Maximize

    def test_bad_sense(self):
        with pytest.raises(ValueError) as (e):
            LpObjective(name='', expression=None, constant=0, sense='')
        assert 'Sense must be one of %s, %s not ' % (Minimize, Maximize) in str(e.value)
        obj = LpObjective(name='', expression=None, constant=0)
        with pytest.raises(ValueError) as (e):
            obj.sense = 'maximize'
        assert 'Sense must be one of %s, %s not ' % (Minimize, Maximize) in str(e.value)