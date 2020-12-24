# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scikits/bvp_solver/tests/test_examples/test_Example4.py
# Compiled at: 2011-07-22 15:26:35
import scikits.bvp_solver, numpy
from numpy.testing import assert_almost_equal
Q = 5.0

def function(X, Y, P):
    LAMBDA = P[0]
    return numpy.array([Y[1],
     -(LAMBDA - 2.0 * Q * numpy.cos(2.0 * X)) * Y[0]])


def function_derivative(X, Y, P):
    LAMBDA = P[0]
    dFdY = numpy.array([[0.0, 1.0],
     [
      -(LAMBDA - 2.0 * Q * numpy.cos(2.0 * X)), 0.0]])
    dFdP = numpy.array([[0],
     [
      -Y[0]]])
    return (
     dFdY, dFdP)


def boundary_conditions(Ya, Yb, P):
    BCa = numpy.array([Ya[1],
     Ya[0] - 1.0])
    BCb = numpy.array([Yb[1]])
    return (BCa, BCb)


def boundary_conditions_derivative(YA, YB, P):
    dBCdYa = numpy.array([[0.0, 1.0],
     [
      1.0, 0.0]])
    dBCdYb = numpy.array([[0.0, 1.0]])
    dBCAdP = numpy.zeros((2, 1))
    dBCBdP = numpy.zeros((1, 1))
    return (
     dBCdYa, dBCdYb, dBCAdP, dBCBdP)


problem = scikits.bvp_solver.ProblemDefinition(num_ODE=2, num_parameters=1, num_left_boundary_conditions=2, boundary_points=(
 0, numpy.pi), function=function, boundary_conditions=boundary_conditions, function_derivative=function_derivative, boundary_conditions_derivative=boundary_conditions_derivative)

def guess(X):
    return numpy.array([numpy.cos(4.0 * X),
     -4.0 * numpy.sin(4.0 * X)])


def test_example4():
    solution = scikits.bvp_solver.solve(problem, solution_guess=guess, parameter_guess=numpy.array([15.0]))
    assert_almost_equal(solution.parameters / 17.097, 1.0, 4)