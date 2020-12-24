# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/loki/.virtualenvs/nls/lib/python2.7/site-packages/nls/solver.py
# Compiled at: 2016-04-23 16:47:57
from __future__ import absolute_import, print_function
from time import time
from .native import nls
from .model import Solution

class AbstractSolver(object):
    """Wrapper(or Facade template) of native fortran subroutine `solve_nls`.
    """

    def __init__(self, model):
        self.model = model
        self.elapsed_time = 0.0

    def __call__(self, num_iters=None):
        if num_iters:
            self.model.setNumberOfIterations(num_iters)
        self.elapsed_time = -time()
        self.solution = Solution(self.model)
        self.solution.setSolution(self.solve(self.model.getTimeStep(), self.model.getSpatialStep(), self.model.getApproximationOrder(), self.model.getNumberOfIterations(), self.model.getPumping(), self.model.getCoefficients(), self.model.getInitialSolution()))
        self.elapsed_time += time()
        self.solution.setElapsedTime(self.elapsed_time)
        return self.solution

    def solve(*args, **kwargs):
        """This method should be override in child classes that specify solver routine(template method pattern).
        """
        raise Exception('AbstractSolver: native solver routine is not passed!')

    def chemicalPotential(self, solution, *args, **kwargs):
        return self.chemicalPotentialRoutine(self.model.getSpatialStep(), self.model.getPumping(), self.model.getCoefficients(), solution)

    def chemicalPotentialRoutine(self, *args, **kwargs):
        """This method should be override in child classses that specify chemical potencial calculation routine.
        """
        raise Exception('AbstractSolver: native solver routine is not passed!')


class Solver1D(AbstractSolver):
    """One dimensional solver that call native Fortran routine that solves NLS equation in axial symmentry in 2D.
    """

    def __init__(self, model):
        super(Solver1D, self).__init__(model)

    def solve(self, *args, **kwargs):
        return nls.solve_nls(*args, **kwargs)

    def chemicalPotentialRoutine(self, *args, **kwargs):
        return nls.chemical_potential_1d(*args, **kwargs)


class Solver2D(AbstractSolver):
    """One dimensional solver that call native Fortran routine that solves NLS equation on a squared grid.
    """

    def __init__(self, model):
        super(Solver2D, self).__init__(model)

    def solve(self, *args, **kwargs):
        return nls.solve_nls_2d(*args, **kwargs)

    def chemicalPotentialRoutine(self, *args, **kwargs):
        return nls.chemical_potential_2d(*args, **kwargs)