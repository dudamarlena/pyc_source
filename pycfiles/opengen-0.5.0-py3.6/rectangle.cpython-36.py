# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/constraints/rectangle.py
# Compiled at: 2020-05-07 20:26:31
# Size of source mod 2**32: 4847 bytes
from .constraint import Constraint
import opengen.functions as fn

class Rectangle(Constraint):
    __doc__ = 'A Rectangle (Box) constraint'

    @classmethod
    def __check_xmin_xmax(cls, xmin, xmax):
        if xmin is None:
            if xmax is None:
                raise Exception('At least one of xmin and xmax must be not None')
            else:
                if xmin is not None:
                    if not isinstance(xmin, list):
                        raise Exception('xmin is neither None nor a list')
                if xmax is not None:
                    if not isinstance(xmax, list):
                        raise Exception('xmax is neither None nor a list')
        else:
            if xmin is not None:
                if xmax is not None:
                    if len(xmin) != len(xmax):
                        raise Exception('xmin and xmax must have equal lengths')
                    for xmin_element, xmax_element in zip(xmin, xmax):
                        if xmin_element > xmax_element:
                            raise Exception('xmin must be <= xmax')

    def __init__(self, xmin, xmax):
        """Construct a new instance of Rectangle

        Args:
            xmin: minimum bounds (can be None)
            xmax: maximum bounds (can be None)

        Raises:
            Exception: if both xmin and xmax is None
              Exception: if xmin/xmax is not None and not a list (wrong type)
            Exception: if xmin and xmax have incompatible lengths
            Exception: if xmin(i) > xmax(i) for some i (empty set)

        Returns:
             A new instance of Rectangle
        """
        Rectangle._Rectangle__check_xmin_xmax(xmin, xmax)
        self._Rectangle__xmin = None if xmin is None else [float(i) for i in xmin]
        self._Rectangle__xmax = None if xmax is None else [float(i) for i in xmax]

    @property
    def xmin(self):
        """Minimum bound"""
        return self._Rectangle__xmin

    @property
    def xmax(self):
        """Maximum bound"""
        return self._Rectangle__xmax

    def dimension(self):
        if self._Rectangle__xmin is not None:
            return len(self._Rectangle__xmin)
        if self._Rectangle__xmax is not None:
            return len(self._Rectangle__xmax)
        raise Exception('Absurd: both xmin and xmax are None!')

    def idx_bound_finite_all(self):
        idx_both_finite = []
        if self._Rectangle__xmin is None or self._Rectangle__xmax is None:
            return idx_both_finite
        else:
            for i in range(self.dimension()):
                xmini = self._Rectangle__xmin[i]
                xmaxi = self._Rectangle__xmax[i]
                if xmini > float('-inf') and xmaxi < float('inf'):
                    idx_both_finite += [i]

            return idx_both_finite

    def idx_infinite_only_xmin(self):
        idx_xmin_infinite = []
        if self._Rectangle__xmax is None:
            return idx_xmin_infinite
        else:
            for i in range(self.dimension()):
                xmini = self._Rectangle__xmin[i] if self._Rectangle__xmin is not None else float('-inf')
                xmaxi = self._Rectangle__xmax[i]
                if xmini == float('-inf') and xmaxi < float('inf'):
                    idx_xmin_infinite += [i]

            return idx_xmin_infinite

    def idx_infinite_only_xmax(self):
        idx_xmin_infinite = []
        if self._Rectangle__xmin is None:
            return idx_xmin_infinite
        else:
            for i in range(self.dimension()):
                xmini = self._Rectangle__xmin[i]
                xmaxi = self._Rectangle__xmax[i] if self._Rectangle__xmax is not None else float('inf')
                if xmaxi == float('inf') and xmini > float('-inf'):
                    idx_xmin_infinite += [i]

            return idx_xmin_infinite

    def distance_squared(self, u):
        idx1 = self.idx_infinite_only_xmin()
        idx2 = self.idx_infinite_only_xmax()
        idx3 = self.idx_bound_finite_all()
        dist_sq = 0.0
        for i in idx1:
            dist_sq += fn.fmax(0.0, u[i] - self._Rectangle__xmax[i]) ** 2

        for i in idx2:
            dist_sq += fn.fmin(0.0, u[i] - self._Rectangle__xmin[i]) ** 2

        for i in idx3:
            dist_sq += fn.fmin(fn.fmax(0.0, u[i] - self._Rectangle__xmax[i]), u[i] - self._Rectangle__xmin[i]) ** 2

        return dist_sq

    def project(self, u):
        raise NotImplementedError()

    def is_convex(self):
        return True

    def is_compact(self):
        if self._Rectangle__xmin is None:
            return False
        if self._Rectangle__xmax is None:
            return False
        for i in range(len(self._Rectangle__xmin)):
            if self._Rectangle__xmin[i] == float('-inf'):
                return False

        for i in range(len(self._Rectangle__xmax)):
            if self._Rectangle__xmax[i] == float('inf'):
                return False