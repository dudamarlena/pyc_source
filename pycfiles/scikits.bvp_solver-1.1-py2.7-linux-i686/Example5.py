# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnsalvatier/Documents/workspace/BVP SOLVERF/src/scikits/bvp_solver/examples/Example5.py
# Compiled at: 2009-11-11 13:38:02
"""
Created on Apr 29, 2009

@author: johnsalvatier
"""
import scikits.bvp_solver, numpy, pylab
from numpy import array
eps = 0.01
gamma = 1.4

def function(t, y):
    term1 = 1.0 / (eps * (1.0 + t ** 2))
    term2 = 0.5 + 0.5 * gamma - 2.0 * eps * t
    arra = array([y[1],
     term1 / y[0] * (term2 * y[0] * y[1] - y[1] / y[0] - 2.0 * t / (1.0 + t ** 2) * (1.0 - 0.5 * (gamma - 1.0) * y[0] ** 2))])
    print arra
    raise ValueError()
    return arra


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


problem_definition = scikits.bvp_solver.ProblemDefinition(num_ODE=2, num_parameters=0, num_left_boundary_conditions=1, boundary_points=(0.0,
                                                                                                                                        1.0), function=function, boundary_conditions=boundary_conditions, function_derivative=function_derivative, boundary_conditions_derivative=boundary_conditions_derivative)
slope = -0.5379
x = numpy.array([0.0, 0.11111, 0.22222, 0.33333, 0.44444, 0.55555, 0.66666, 0.77778, 0.88888, 1.0])
print numpy.array([0.9129 + slope * x, x * 0 + slope]).shape
solution = scikits.bvp_solver.solve(bvp_problem=problem_definition, initial_mesh=x, solution_guess=[
 0.9129 + slope * x, x * 0 + slope], trace=2)
points = numpy.linspace(0, 1, 200)
pylab.plot(points, solution(points)[0, :], '-')
pylab.plot(points, solution(points)[1, :], '-')
pylab.show()