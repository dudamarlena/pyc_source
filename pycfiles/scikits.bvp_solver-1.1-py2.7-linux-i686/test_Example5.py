# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scikits/bvp_solver/tests/test_examples/test_Example5.py
# Compiled at: 2011-07-22 15:26:35
"""
Created on Apr 29, 2009

@author: johnsalvatier
"""
import scikits.bvp_solver, numpy
from numpy import array
from numpy.testing import assert_almost_equal
import example5data as data, os, testing
eps = 0.01
gamma = 1.4

def function(t, y):
    term1 = 1.0 / (eps * (1.0 + t ** 2))
    term2 = 0.5 + 0.5 * gamma - 2.0 * eps * t
    return array([y[1],
     term1 / y[0] * (term2 * y[0] * y[1] - y[1] / y[0] - 2.0 * t / (1.0 + t ** 2) * (1.0 - 0.5 * (gamma - 1.0) * y[0] ** 2))])


def boundary_conditions(Ya, Yb):
    BCa = array([Ya[0] - 0.9129])
    BCb = array([Yb[0] - 0.375])
    return (BCa, BCb)


def function_derivative(t, y):
    term1 = 1.0 / (eps * (1.0 + t ** 2))
    term2 = 0.5 + 0.5 * gamma - 2.0 * eps * t
    dFdY = array([[0.0, 1.0],
     [
      term1 * (2.0 * y[1] / y[0] ** 3 + 2.0 * t / ((1.0 + t ** 2) * y[0] ** 2) + t / (1.0 + t ** 2) * (gamma - 1.0)),
      term1 / y[0] * (term2 * y[0] - 1.0 / y[0])]])
    return dFdY


def boundary_conditions_derivative(Ya, Yb):
    dBCadYa = array([[1.0, 0.0]])
    dBCbdYb = array([[1.0, 0.0]])
    return (
     dBCadYa, dBCbdYb)


def setup_module(module):
    module.problem_definition = scikits.bvp_solver.ProblemDefinition(num_ODE=2, num_parameters=0, num_left_boundary_conditions=1, boundary_points=(0.0,
                                                                                                                                                   1.0), function=function, boundary_conditions=boundary_conditions, function_derivative=function_derivative, boundary_conditions_derivative=boundary_conditions_derivative)
    slope = -0.5379
    x = array([0.0, 0.11111, 0.22222, 0.33333, 0.44444, 0.55555, 0.66666, 0.77778, 0.88888, 1.0])
    module.solution = scikits.bvp_solver.solve(bvp_problem=module.problem_definition, initial_mesh=x, solution_guess=[
     0.9129 + slope * x, x * 0 + slope])


def test_example5_solution_correctness():
    testing.assert_solution_matches_data_eval(solution, data)
    testing.assert_solution_matches_data_calculated(solution, data)


def test_solution_saving():
    solution.save('test_solution.sol')
    solution2 = scikits.bvp_solver.Solution.load('test_solution.sol')
    os.remove('test_solution.sol')
    solution3 = scikits.bvp_solver.solve(bvp_problem=problem_definition, solution_guess=solution2)