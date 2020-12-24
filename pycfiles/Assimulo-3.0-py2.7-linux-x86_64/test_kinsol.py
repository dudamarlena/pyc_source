# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/tests/solvers/test_kinsol.py
# Compiled at: 2017-12-28 04:09:42
import nose
from assimulo import testattr
from assimulo.solvers.kinsol import *
from assimulo.problem import Algebraic_Problem
from assimulo.exception import *

class Test_KINSOL:

    @testattr(stddist=True)
    def test_problem_name_attribute(self):
        res = lambda y: y
        model = Algebraic_Problem(res, 1)
        assert model.name == '---'
        model = Algebraic_Problem(res, 1, name='Test')
        assert model.name == 'Test'

    @testattr(stddist=True)
    def test_properties_simple(self):
        res = lambda y: y
        model = Algebraic_Problem(res, 1)
        solver = KINSOL(model)
        solver.max_iter = 150
        assert solver.max_iter == 150
        solver.no_initial_setup = True
        assert solver.no_initial_setup == True
        solver.max_solves_between_setup_calls = 15
        assert solver.max_solves_between_setup_calls == 15
        solver.max_newton_step = 1.0
        assert solver.max_newton_step == 1.0
        solver.no_min_epsilon = True
        assert solver.no_min_epsilon == True
        solver.max_beta_fails = 15
        assert solver.max_beta_fails == 15