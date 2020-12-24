# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Felipe\surropt\build\lib\surropt\caballero\problem.py
# Compiled at: 2019-11-06 13:11:24
# Size of source mod 2**32: 8482 bytes
import numpy as np
from ..core.options import ProcedureOptions
__all__ = [
 'CaballeroOptions', 'is_inside_hypercube']

class CaballeroOptions(ProcedureOptions):
    __doc__ = 'Options structure for the Caballero class algorithm.\n\n    Parameters\n    ----------\n    max_fun_evals : int, optional\n        Maximum number of black box function evaluations, by default 500.\n\n    feasible_tol : float, optional\n        Feasibility tolerance for the model constraints g(x) <= tol, by default\n        1e-06.\n\n    penalty_factor : float, optional\n        Value to penalize the objective function when its value returned by the\n        black box model indicates that is a infeasible result (note that by\n        infeasible it is referring to whether or not the sampling converged for\n        that case, not optimization feasibility), by default None.\n\n        See this property notes for more info.\n\n    ref_tol : float, optional\n        Refinement tolerance specification (tol1), by default 1e-4.\n\n    term_tol : float, optional\n        Termination tolerance specification (tol2), by default 1e-5. Has to be\n        lesser than `ref_tol`.\n\n    first_factor : float, optional\n        First contraction factor specification, by default 0.6. Has to be\n        between 0 and 1.\n\n    second_factor : float, optional\n        Subsequent contraction factor specification, by default 0.4. Has to be\n        between 0 and 1. Has to be lesser than `first_factor`.\n\n    contraction_tol : float, optional\n        Maximum contraction size that the refinement hypercube can achieve\n        when compared to the original domain, by default 1e-4.\n\n        See this property notes for more information.\n    '

    @property
    def penalty_factor(self):
        """Value to penalize the objective function when its value returned by
        the black box model indicates that is a infeasible result (note that
        "infeasible result" it is referring to whether or not the sampling 
        converged for that case, not constraint feasibility), by default None.

        The value set for the penalty factor is simply summed to the objective
        function value in order to make the optimization procedure avoid
        sampling in the known infeasible regionself.

        If this value is set to None, the procedure will automatically chose 
        the highest value of the objective function in the initial sampling as
        the penalty factor."""
        return self._penalty_factor

    @penalty_factor.setter
    def penalty_factor(self, value):
        self._penalty_factor = value

    @property
    def first_factor(self):
        """First contraction factor specification."""
        return self._first_factor

    @first_factor.setter
    def first_factor(self, value):
        if isinstance(value, float):
            if 0.0 < value < 1.0:
                self._first_factor = value
            else:
                raise ValueError("'first_factor' value has to be in the range (0, 1).")
        else:
            raise ValueError("'first_factor' has to be a float.")

    @property
    def second_factor(self):
        """Second contraction factor specification."""
        return self._second_factor

    @second_factor.setter
    def second_factor(self, value):
        if isinstance(value, float):
            if 0.0 < value < 1.0:
                self._second_factor = value
            else:
                raise ValueError("'second_factor' value has to be in the range (0, 1).")
        else:
            raise ValueError("'second_factor' has to be a float.")

    @property
    def ref_tol(self):
        """Refinement tolerance specification (tol1)."""
        return self._ref_tol

    @ref_tol.setter
    def ref_tol(self, value):
        if isinstance(value, float):
            if value > 0.0:
                self._ref_tol = value
            else:
                raise ValueError("'ref_tol' value has to be a positive float.")
        else:
            raise ValueError("'ref_tol' has to be a float.")

    @property
    def term_tol(self):
        """Termination tolerance specification (tol2)."""
        return self._term_tol

    @term_tol.setter
    def term_tol(self, value):
        if isinstance(value, float):
            if value > 0.0:
                self._term_tol = value
            else:
                raise ValueError("'term_tol' value has to be a positive float.")
        else:
            raise ValueError("'term_tol' has to be a float.")

    @property
    def contraction_tol(self):
        """Maximum contraction size that the refinement hypercube can achieve
        when compared to the original domain.

        The ratio between the current refined hypercube range and the original
        domain range can't be lesser than `contraction_tol`. After the ratio
        reaches this value, no more contractions will be perfomed."""
        return self._contraction_tol

    @contraction_tol.setter
    def contraction_tol(self, value):
        if isinstance(value, float):
            if value > 0.0:
                self._contraction_tol = value
            else:
                raise ValueError("'contraction_tol' value has to be a positive float.")
        else:
            raise ValueError("'contraction_tol' has to be a float.")

    def __init__(self, max_fun_evals=500, feasible_tol=1e-06, penalty_factor=None, ref_tol=0.0001, term_tol=1e-05, first_factor=0.6, second_factor=0.4, contraction_tol=0.0001):
        super().__init__(max_fun_evals=max_fun_evals, feasible_tol=feasible_tol)
        self.penalty_factor = penalty_factor
        self.first_factor = first_factor
        self.second_factor = second_factor
        self.ref_tol = ref_tol
        self.term_tol = term_tol
        self.contraction_tol = contraction_tol
        self.check_options_setup()

    def check_options_setup(self):
        if self.first_factor <= self.second_factor:
            raise ValueError("'first_factor' has to be greater than 'second_factor'.")
        if self.ref_tol <= self.term_tol:
            raise ValueError("'ref_tol' has to be greater than 'term_tol'.")


def is_inside_hypercube(point: np.ndarray, lb: np.ndarray, ub: np.ndarray, tol: float=1e-08):
    """Determines if a `point` is inside a hypercube following a specified
    tolerance.

    Parameters
    ----------
    point : np.ndarray
        Point to be checked (1D array).

    lb : np.ndarray
        Hypercube lower bound (1D array).

    ub : np.ndarray
        Hypercube upper bound(1D array).

    tol : float, optional
        Tolerance value to accept whether or not `point` is at the limit.
        Default is 1e-8. (This value is a percentage of domain range.)
    """
    lbf = np.zeros(lb.shape)
    ubf = ub - lb
    pointf = point - lb
    if np.any(np.greater(pointf, ubf)) or np.any(np.less(pointf, lbf)):

        def arr2str_fcn(x):
            return np.array2string(x, precision=4, separator='\t',
              sign=' ')

        err_msg = 'Point: {0}\nLB: {1}\nUB: {2}'.format(arr2str_fcn(point), arr2str_fcn(lb), arr2str_fcn(ub))
        raise ValueError('The point is outside the hypercube.\n' + err_msg)
    else:
        if np.any(np.abs((ubf - pointf) / ubf) <= tol) or np.any(np.abs((pointf - lbf) / ubf <= tol)):
            return False
        else:
            return True