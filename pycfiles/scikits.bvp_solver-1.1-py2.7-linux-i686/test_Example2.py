# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scikits/bvp_solver/tests/test_examples/test_Example2.py
# Compiled at: 2011-07-22 15:26:35
import scikits.bvp_solver, numpy
from numpy.testing import assert_almost_equal
import nose, example2data as data, testing
AR = numpy.array([2.03464, 2.11986, 2.11997, 2.11997])

def function1(X, Y):
    return numpy.array([Y[1], -(X * Y[0] - 1.0) * Y[0]])


def dfunction1(X, Y):
    PD = numpy.zeros((2, 2))
    PD[(0, 1)] = 1.0
    PD[(1, 0)] = 1.0 - 2 * X * Y[0]
    return PD


def boundary_conditions1(YA, YB):
    BCA = numpy.zeros(1)
    BCB = numpy.zeros(1)
    BCA[0] = YA[1]
    BCB[0] = YB[0] + YB[1]
    return (
     BCA, BCB)


def guess_y1(X):
    Y = numpy.zeros(2)
    if X <= 1.5:
        Y[0] = 2
        Y[1] = 0
    else:
        Y[0] = 2.0 * numpy.exp(1.5 - X)
        Y[1] = -Y[0]
    return Y


singular_term = numpy.zeros((2, 2))
singular_term[(1, 1)] = -4.0
L = [
 5, 8, 10, 20]

def test_example2():
    solutionList = []
    problemList = []
    for i in range(4):
        problemList.append(scikits.bvp_solver.ProblemDefinition(num_ODE=2, num_parameters=0, num_left_boundary_conditions=1, boundary_points=(
         0, L[i]), function=function1, boundary_conditions=boundary_conditions1, function_derivative=dfunction1))
        if i == 0:
            solutionList.append(scikits.bvp_solver.solve(problemList[i], solution_guess=guess_y1, singular_term=singular_term))
        else:
            solutionList.append(solutionList[(i - 1)].extend(0, L[i]))
            nose.tools.assert_raises(ValueError, solutionList[i], numpy.array([0]))
            solutionList[i] = scikits.bvp_solver.solve(problemList[i], solution_guess=solutionList[i], singular_term=singular_term)
        if i == 2:
            testing.assert_solution_matches_data_eval(solutionList[i], data, 4)
            testing.assert_solution_matches_data_calculated(solutionList[i], data, 2)

    for i in range(4):
        assert_almost_equal(solutionList[i](0.0)[(0, 0)], AR[i], 4)