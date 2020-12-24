# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scikits/bvp_solver/tests/test_examples/testing.py
# Compiled at: 2011-07-22 15:26:35
"""
Created on Aug 30, 2009

@author: johnsalvatier
"""
from numpy.testing import assert_almost_equal

def assert_solution_matches_data_eval(solution, data, precision=4):
    yEval, yDerivativeEval = solution(data.xEval, eval_derivative=True)
    if 'yEval' in data.__dict__:
        assert_almost_equal(yEval, data.yEval, precision)
    if 'yDerivativeEval' in data.__dict__:
        assert_almost_equal(yDerivativeEval, data.yDerivativeEval, precision)


def assert_solution_matches_data_calculated(solution, data, precision=4):
    assert_almost_equal(solution.mesh, data.xSol, precision)
    assert_almost_equal(solution.solution, data.ySol, precision)
    assert_almost_equal(solution.work, data.workSol, precision)
    assert_almost_equal(solution.iwork, data.iworkSol, precision)