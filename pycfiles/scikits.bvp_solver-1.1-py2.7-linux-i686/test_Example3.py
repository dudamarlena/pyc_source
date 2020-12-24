# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scikits/bvp_solver/tests/test_examples/test_Example3.py
# Compiled at: 2011-07-22 15:26:35
import scikits.bvp_solver, numpy
from numpy.testing import assert_almost_equal
import example3data as data, nose, testing
eps = 0.1

def function2(X, Y, P):
    return numpy.array([(numpy.sin(X) ** 2 - P[0] * numpy.sin(X) ** 4 / Y[0]) / eps])


def dfunction2(X, Y, P):
    dFdY = numpy.zeros((1, 1))
    dFdY[(0, 0)] = P[0] * numpy.sin(X) ** 4 / Y[0] ** 2 / eps
    dFdP = numpy.zeros((1, 1))
    dFdP[(0, 0)] = -numpy.sin(X) ** 4 / Y[0] / eps
    return (
     dFdY, dFdP)


def boundary_conditions2(YA, YB, P):
    BCA = numpy.zeros(1)
    BCB = numpy.zeros(1)
    BCA[0] = YA[0] - 1.0
    BCB[0] = YB[0] - 1.0
    return (
     BCA, BCB)


def dbconditions2(YA, YB, P):
    DYA = numpy.zeros((1, 1))
    DYA[(0, 0)] = 1
    DYB = numpy.zeros((1, 1))
    DYB[(0, 0)] = 1
    DAP = numpy.zeros((1, 1))
    DBP = numpy.zeros((1, 1))
    return (DYA, DYB, DAP, DBP)


problem = 0
solution = 0

def setup_module(test_example3):
    test_example3.problem = scikits.bvp_solver.ProblemDefinition(num_ODE=1, num_parameters=1, num_left_boundary_conditions=1, boundary_points=(
     -numpy.pi / 2.0, numpy.pi / 2.0), function=function2, boundary_conditions=boundary_conditions2, function_derivative=dfunction2, boundary_conditions_derivative=dbconditions2)
    test_example3.solution = scikits.bvp_solver.solve(problem, solution_guess=0.5, initial_mesh=numpy.linspace(test_example3.problem.boundary_points[0], test_example3.problem.boundary_points[1], 21), parameter_guess=1)


def test_example3_param():
    assert_almost_equal(solution.parameters / data.lambdap, 1.0, 5)


def test_example3_solution_correctness():
    testing.assert_solution_matches_data_eval(solution, data)
    testing.assert_solution_matches_data_calculated(solution, data)


def test_evaluateOutOfBounds():
    nose.tools.assert_raises(ValueError, solution, numpy.array([6]))


def test_extension():
    solution2 = solution.extend(-numpy.pi / 2.0, numpy.pi / 2.0 + 1.0)