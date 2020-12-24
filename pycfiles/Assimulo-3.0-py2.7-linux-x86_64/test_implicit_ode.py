# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/tests/test_implicit_ode.py
# Compiled at: 2017-12-28 04:09:42
import nose
from assimulo import testattr
from assimulo.implicit_ode import *
from assimulo.problem import Implicit_Problem
from assimulo.exception import *

class Test_Implicit_ODE:

    @testattr(stddist=True)
    def test_elapsed_step_time(self):
        res = lambda t, y, yd: y
        prob = Implicit_Problem(res, 0.0, 0.0)
        solv = Implicit_ODE(prob)
        assert solv.get_elapsed_step_time() == -1.0

    @testattr(stddist=True)
    def test_problem_name_attribute(self):
        res = lambda t, y, yd: y
        prob = Implicit_Problem(res, 0.0, 0.0)
        assert prob.name == '---'
        prob = Implicit_Problem(res, 0.0, 0.0, name='Test')
        assert prob.name == 'Test'

    @testattr(stddist=True)
    def test_re_init(self):
        res = lambda t, y, yd: y
        prob = Implicit_Problem(res, 0.0, 0.0)
        solv = Implicit_ODE(prob)
        assert solv.t == 0.0
        assert solv.y[0] == 0.0
        assert solv.yd[0] == 0.0
        solv.re_init(1.0, 2.0, 3.0)
        assert solv.t == 1.0
        assert solv.y[0] == 2.0
        assert solv.yd[0] == 3.0