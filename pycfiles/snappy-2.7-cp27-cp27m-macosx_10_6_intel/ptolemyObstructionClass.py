# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/ptolemy/ptolemyObstructionClass.py
# Compiled at: 2017-05-26 08:27:22
from __future__ import print_function

class PtolemyObstructionClass(object):
    """
    Represents an obstruction cocycle of a pSL(n,C) representation as
    described in Definition 1.7 of
    
    Garoufalidis, Thurston, Zickert
    The Complex Volume of SL(n,C)-Representations of 3-Manifolds
    http://arxiv.org/abs/1111.2828

    To generate such an obstruction class, call:

    >>> from snappy import Manifold
    >>> M = Manifold("4_1")
    >>> cs = M.ptolemy_obstruction_classes()

    Print out the values:
    >>> for c in cs: print(c)
    PtolemyObstructionClass(s_0_0 - 1, s_1_0 - 1, s_2_0 - 1, s_3_0 - 1, s_0_0 - s_0_1, s_1_0 - s_3_1, s_2_0 - s_2_1, s_3_0 - s_1_1)
    PtolemyObstructionClass(s_0_0 + 1, s_1_0 - 1, s_2_0 - 1, s_3_0 + 1, s_0_0 - s_0_1, s_1_0 - s_3_1, s_2_0 - s_2_1, s_3_0 - s_1_1)
    """

    def __init__(self, manifold, index, H2_element, explain_basis, identified_face_classes):
        self._manifold = manifold
        self._index = index
        self._H2_element = H2_element
        self._explain_basis = explain_basis
        self._identified_face_classes = identified_face_classes

        def H2_element_entry_to_identified_variable(entry, variable):
            return (
             (-1) ** entry, 0, variable, 1)

        self.identified_variables = [ H2_element_entry_to_identified_variable(entry, variable) for entry, variable in zip(H2_element, explain_basis)
                                    ] + [ (+1, 0, var1, var2) for sign, power, var1, var2 in self._identified_face_classes
                                        ]

    def _checkManifoldAndN(self, manifold, N):
        assert self._manifold is not None and manifold == self._manifold, 'PtolemyObstructionClass for wrong manifold'
        assert N % 2 == 0, 'PtolemyObstructionClass only makes sense for even N, try PtolemyGeneralizedObstructionClass'
        return

    def __repr__(self):

        def to_string(i):
            sign, power, var1, var2 = i
            var2 = str(var2)
            assert sign in [+1, -1]
            if sign == +1:
                return var1 + ' - ' + var2
            else:
                return var1 + ' + ' + var2

        return 'PtolemyObstructionClass(%s)' % (', ').join([ to_string(i) for i in self.identified_variables ])