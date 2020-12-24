# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python3/pracmln/mln/learning/ll.py
# Compiled at: 2018-04-24 04:48:32
# Size of source mod 2**32: 3946 bytes
from dnutils import ProgressBar
from .common import *
from ..grounding.default import DefaultGroundingFactory
from ..constants import HARD
from ..errors import SatisfiabilityException

class LL(AbstractLearner):
    __doc__ = '\n    Exact Log-Likelihood learner.\n    '

    def __init__(self, mrf, **params):
        AbstractLearner.__init__(self, mrf, **params)
        self._stat = None
        self._ls = None
        self._eworld_idx = None
        self._lastw = None

    def _prepare(self):
        self._compute_statistics()

    def _l(self, w):
        """
        computes the likelihoods of all possible worlds under weights w
        """
        if self._lastw is None or list(w) != self._lastw:
            self._lastw = list(w)
            expsums = []
            for fvalues in self._stat:
                s = 0
                hc_violation = False
                for fidx, val in fvalues.items():
                    if self.mrf.mln.formulas[fidx].weight == HARD:
                        if val == 0:
                            hc_violation = True
                            break
                    else:
                        s += val * w[fidx]

                if hc_violation:
                    expsums.append(0)
                else:
                    expsums.append(exp(s))

            z = sum(expsums)
            if z == 0:
                raise SatisfiabilityException('MLN is unsatisfiable: probability masses of all possible worlds are zero.')
            self._ls = [v / z for v in expsums]
        return self._ls

    def _f(self, w):
        ls = self._l(w)
        return numpy.log(ls[self._eworld_idx])

    def _grad(self, w):
        ls = self._l(w)
        grad = numpy.zeros(len(self.mrf.formulas), numpy.float64)
        for widx, values in enumerate(self._stat):
            for fidx, count in values.items():
                if widx == self._eworld_idx:
                    grad[fidx] += count
                grad[fidx] -= count * ls[widx]

        return grad

    def _compute_statistics(self):
        self._stat = []
        grounder = DefaultGroundingFactory(self.mrf)
        eworld = list(self.mrf.evidence)
        if self.verbose:
            bar = ProgressBar(steps=self.mrf.countworlds(), color='green')
        for widx, world in self.mrf.iterallworlds():
            if self.verbose:
                bar.label(str(widx))
                bar.inc()
            values = {}
            self._stat.append(values)
            if self._eworld_idx is None and world == eworld:
                self._eworld_idx = widx
            for gf in grounder.itergroundings():
                truth = gf(world)
                if truth != 0:
                    values[gf.idx] = values.get(gf.idx, 0) + truth