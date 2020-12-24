# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/numeric/replicators.py
# Compiled at: 2006-08-15 14:26:21
"""Numerical replicators"""
from evogrid.common.replicators import DomainedReplicator
from evogrid.numeric.interfaces import IVectorReplicator
from numpy import array
from zope.interface import implements

class VectorReplicator(DomainedReplicator):
    """DomainedReplicator with a numpy array as candidate solution"""
    __module__ = __name__
    implements(IVectorReplicator)

    def _get_cs(self):
        return self._candidate_solution

    def _set_cs(self, cs):
        if cs is not None:
            cs = array(cs)
        super(VectorReplicator, self)._set_cs(cs)
        return

    candidate_solution = property(_get_cs, _set_cs)

    def __eq__(self, other):
        """Test candidate solution equality

        All vector parameters must be equal.
        """
        return (self.candidate_solution == other.candidate_solution).all()