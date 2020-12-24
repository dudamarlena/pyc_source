# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scikits/bvp_solver/tests/test_examples/test_TutorialExample.py
# Compiled at: 2011-07-22 15:26:35
"""
First we import scikits.bvp_solver and numpy because the callback functions must return numpy arrays.
"""
import scikits.bvp_solver, numpy

def test_quickStartExample():
    T10 = 130
    T2Ahx = 70
    Ahx = 5
    U = 1.0

    def function(a, T):
        q = (T[0] - T[1]) * U
        return numpy.array([-q,
         q / -2.0])

    def boundary_conditions(Ta, Tb):
        return (
         numpy.array([Ta[0] - T10]),
         numpy.array([Tb[1] - T2Ahx]))

    problem = scikits.bvp_solver.ProblemDefinition(num_ODE=2, num_parameters=0, num_left_boundary_conditions=1, boundary_points=(
     0, Ahx), function=function, boundary_conditions=boundary_conditions)
    solution = scikits.bvp_solver.solve(problem, solution_guess=(
     (T10 + T2Ahx) / 2.0,
     (T10 + T2Ahx) / 2.0))
    A = numpy.linspace(0, Ahx, 45)
    T = solution(A)