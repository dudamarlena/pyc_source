# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nyga/work/code/pracmln/python3/pracmln/mln/inference/maxwalk.py
# Compiled at: 2018-04-24 04:48:32
# Size of source mod 2**32: 5102 bytes
import random
from collections import defaultdict
from dnutils import ProgressBar
from .mcmc import MCMCInference
from ..constants import HARD, ALL
from ..grounding.fastconj import FastConjunctionGrounding
from ...logic.common import Logic

class SAMaxWalkSAT(MCMCInference):
    """SAMaxWalkSAT"""

    def __init__(self, mrf, queries=ALL, state=None, **params):
        MCMCInference.__init__(self, mrf, queries, **params)
        if state is None:
            self.state = self.random_world(self.mrf.evidence)
        else:
            self.state = state
        self.sum = 0
        self.var2gf = defaultdict(set)
        self.weights = list(self.mrf.mln.weights)
        formulas = []
        for f in self.mrf.formulas:
            if f.weight < 0:
                f_ = self.mrf.mln.logic.negate(f)
                f_.weight = -f.weight
                formulas.append(f_.nnf())

        grounder = FastConjunctionGrounding(mrf, formulas=formulas, simplify=True, unsatfailure=True)
        for gf in grounder.itergroundings():
            if isinstance(gf, Logic.TrueFalse):
                pass
            else:
                vars_ = set([self.mrf.variable(a).idx for a in gf.gndatoms()])
                for v in vars_:
                    self.var2gf[v].add(gf)

                self.sum += (self.hardw if gf.weight == HARD else gf.weight) * (1 - gf(self.state))

    @property
    def thr(self):
        return self._params.get('thr', 0)

    @property
    def hardw(self):
        return self._params.get('hardw', 10)

    @property
    def maxsteps(self):
        return self._params.get('maxsteps', 500)

    def _run(self):
        i = 0
        i_max = self.maxsteps
        thr = self.thr
        if self.verbose:
            bar = ProgressBar(steps=i_max, color='green')
        while i < i_max and self.sum > self.thr:
            var = self.mrf.variables[random.randint(0, len(self.mrf.variables) - 1)]
            evdict = var.value2dict(var.evidence_value(self.mrf.evidence))
            valuecount = var.valuecount(evdict)
            if valuecount == 1:
                pass
            else:
                sum_before = 0
                for gf in self.var2gf[var.idx]:
                    sum_before += (self.hardw if gf.weight == HARD else gf.weight) * (1 - gf(self.state))

                validx = random.randint(0, valuecount - 1)
                value = [v for _, v in var.itervalues(evdict)][validx]
                oldstate = list(self.state)
                var.setval(value, self.state)
                sum_after = 0
                for gf in self.var2gf[var.idx]:
                    sum_after += (self.hardw if gf.weight == HARD else gf.weight) * (1 - gf(self.state))

                keep = False
                improvement = sum_after - sum_before
                if improvement < 0 or sum_after <= thr:
                    prob = 1.0
                    keep = True
                else:
                    prob = (1.0 - min(1.0, abs(improvement / self.sum))) * (1 - float(i) / i_max)
                    keep = random.uniform(0.0, 1.0) <= prob
                if keep:
                    self.sum += improvement
                else:
                    self.state = oldstate
                i += 1
                if self.verbose:
                    bar.label('sum = %f' % self.sum)
                    bar.inc()

        if self.verbose:
            print('SAMaxWalkSAT: %d iterations, sum=%f, threshold=%f' % (i, self.sum, self.thr))
        self.mrf.mln.weights = self.weights
        return dict([(str(q), self.state[q.gndatom.idx]) for q in self.queries])