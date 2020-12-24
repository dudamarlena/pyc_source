# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/sharing/interfaces.py
# Compiled at: 2006-07-29 16:49:40
"""Sharing aware components
"""
from evogrid.interfaces import IComparator
from zope.interface import Interface

class IDistance(Interface):
    """Distance function for some space M

    Any implementation should be a function from M x M -> R+ that satisfies the
    following conditions:

      1- For all x, y in M x M:         d(x, y) == 0 <=> x == y
      2- For all x, y in M x M:         d(x, y) == d(y, x)
      3- For all x, y, z in M x M x M:  d(x, z) <= d(x, y) + d(y, z)

    In some cases, building a true distance can be tedious. Most of the time, the
    sharing components require only the first two rules to be respected and the
    third rule "somewhat" respected to work properly. Don't forget that we are
    using evolutionary computation to find good solutions, not to formally prove
    that the solutions we get are the best.

    The M space is usually the search space (of all possible
    ``candidate_solution``) but can also be the fitness landscape in multi
    objective optimization.
    """
    __module__ = __name__

    def __call__(x1, X2):
        """Compute d(x1, x2) == d(x2, x1)"""
        pass


class ISharingAwareComparator(IComparator):
    """Comparator that shares evaluations according to a distance

    Judgements depend on a sharing context (eg some pool) and a distance component.
    Replicators that are near many other replicators of the pool have considered
    less interesting than replicators that loners.

    When comparing replicators with either ``cmp`` or ``max``, replicators are
    first taken out of the sharing context (not affecting the underlying pool
    if any). This is usefull for replacers to be able to replace a replicator
    in the pool by a better one without being affected by the one that might
    go away.
    """
    __module__ = __name__

    def distance(rep1, rep2):
        """Compute the distance between ``rep1`` and ``rep2``

        ``sharing.distance(rep1, rep2)`` is a strictly positive float unless
        ``rep1.candidate_solution == rep2.candidate_solution``. In that case
        the distance is ``0.0``

        raises ValueError if ``rep1`` or ``rep2`` does not belong to the
        context
        """
        pass

    def share_evaluation(rep, pool=None):
        """Return the evaluation of replicator ``rep`` in the w.r.t. sharing

        Replicators that are close to many other replicators are devaluated
        whereas isolated ones get higher scores.

        The value of ``rep.evaluation`` is not affected by this operation.

        The optional ``pool`` argument can be used to specify an explicit
        sharing context
        """
        pass