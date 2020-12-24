# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scikits/bvp_solver/tests/test_Solution.py
# Compiled at: 2011-07-22 15:26:36
import scikits.bvp_solver, numpy
from numpy.testing import assert_almost_equal
import nose

def functionGood(X, Y, P):
    return numpy.array([0])


def dfunctionGood(X, Y, P):
    dFdY = numpy.zeros((1, 1))
    dFdP = numpy.zeros((1, 1))
    return (
     dFdY, dFdP)


def boundary_conditionsGood(YA, YB, P):
    BCA = YA[0] - numpy.ones(1)
    BCB = YB[0] - numpy.zeros(1)
    return (
     BCA, BCB)


def dbconditionsGood(YA, YB, P):
    DYA = numpy.ones((1, 1))
    DYB = numpy.ones((1, 1))
    DAP = numpy.zeros((1, 1))
    DBP = numpy.zeros((1, 1))
    return (
     DYA, DYB, DAP, DBP)


def test_failure():
    problem1 = scikits.bvp_solver.ProblemDefinition(num_ODE=1, num_parameters=1, num_left_boundary_conditions=1, boundary_points=(
     -numpy.pi / 2.0, numpy.pi / 2.0), function=functionGood, boundary_conditions=boundary_conditionsGood, function_derivative=dfunctionGood, boundary_conditions_derivative=dbconditionsGood)
    nose.tools.assert_raises(ValueError, scikits.bvp_solver.solve, problem1, solution_guess=0, initial_mesh=numpy.linspace(problem1.boundary_points[0], problem1.boundary_points[1], 21), parameter_guess=1)
    solution = scikits.bvp_solver.solve(problem1, solution_guess=0, initial_mesh=numpy.linspace(problem1.boundary_points[0], problem1.boundary_points[1], 21), parameter_guess=1, error_on_fail=False)
    nose.tools.assert_raises(ValueError, solution, 0)