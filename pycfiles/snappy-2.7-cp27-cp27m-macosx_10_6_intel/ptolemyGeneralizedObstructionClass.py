# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/ptolemy/ptolemyGeneralizedObstructionClass.py
# Compiled at: 2019-07-15 23:56:54
from __future__ import print_function
from . import matrix
from .polynomial import Polynomial
from ..pari import pari

class PtolemyGeneralizedObstructionClass(object):
    """
    Represents an obstruction cocycle of a PSL(n,C) representation in
    H^2(M,partial M;Z/n).

    >>> from snappy import Manifold
    >>> M = Manifold("m004")

    Create an obstruction class, this has to be in the kernel of d^2
    >>> c = PtolemyGeneralizedObstructionClass([2,0,0,1])

    For better accounting, give it an index
    >>> c = PtolemyGeneralizedObstructionClass([2,0,0,1], index = 1)

    Get corresponding ptolemy variety
    >>> p=M.ptolemy_variety(N = 3, obstruction_class = c)

    Canonical filename base
    >>> p.filename_base()
    'm004__sl3_c1'

    Now pick something not in the kernel
    >>> c = PtolemyGeneralizedObstructionClass([1,0,0,1])
    >>> p=M.ptolemy_variety(N = 3, obstruction_class = c)
    Traceback (most recent call last):
       ...
    AssertionError: PtolemyGeneralizedObstructionClass not in kernel of d2
    """

    def __init__(self, H2_class, index=None, N=None, manifold=None):
        self.H2_class = H2_class
        self._index = index
        self._N = N
        self._manifold = manifold

    def _checkManifoldAndN(self, manifold, N):
        if self._manifold is not None:
            assert manifold == self._manifold, 'PtolemyGeneralizedObstructionClass for wrong manifold'
            assert self._N is not None and N == self._N, 'PtolemyGeneralizedObstructionClass for wrong N'
        assert len(self.H2_class) == 2 * manifold.num_tetrahedra(), 'PtolemyGeneralizedObstructionClass does not match number of face classes'
        chain_d3, dummy_rows, dummy_columns = manifold._ptolemy_equations_boundary_map_3()
        cochain_d2 = matrix.matrix_transpose(chain_d3)
        assert matrix.is_vector_zero(matrix.vector_modulo(matrix.matrix_mult_vector(cochain_d2, self.H2_class), N)), 'PtolemyGeneralizedObstructionClass not in kernel of d2'
        return

    def _is_non_trivial(self, N):
        for h in self.H2_class:
            if h % N != 0:
                return True

        return False

    def _get_equation_for_u(self, N):
        if self._is_non_trivial(N):
            if N == 2:
                return (
                 2, [])
            else:
                cyclo = Polynomial.parse_string(str(pari.polcyclo(N, 'u')))
                return (N, [cyclo])

        else:
            return (
             1, [])

    def __repr__(self):
        return 'PtolemyGeneralizedObstructionClass(%s)' % self.H2_class