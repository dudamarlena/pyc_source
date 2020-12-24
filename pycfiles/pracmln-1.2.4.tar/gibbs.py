# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python2/pracmln/mln/inference/gibbs.py
# Compiled at: 2018-04-24 04:48:32
import random
from collections import defaultdict
import numpy
from dnutils import ProgressBar
from pracmln.logic.common import Logic
from pracmln.mln.constants import ALL
from pracmln.mln.grounding.fastconj import FastConjunctionGrounding
from pracmln.mln.inference.mcmc import MCMCInference

class GibbsSampler(MCMCInference):

    def __init__(self, mrf, queries=ALL, **params):
        MCMCInference.__init__(self, mrf, queries, **params)
        self.var2gf = defaultdict(set)
        grounder = FastConjunctionGrounding(mrf, simplify=True, unsatfailure=True, cache=None)
        for gf in grounder.itergroundings():
            if isinstance(gf, Logic.TrueFalse):
                continue
            vars_ = set(map(lambda a: self.mrf.variable(a).idx, gf.gndatoms()))
            for v in vars_:
                self.var2gf[v].add(gf)

        return

    @property
    def chains(self):
        return self._params.get('chains', 1)

    @property
    def maxsteps(self):
        return self._params.get('maxsteps', 500)

    class Chain(MCMCInference.Chain):

        def __init__(self, infer, queries):
            MCMCInference.Chain.__init__(self, infer, queries)
            mrf = infer.mrf

        def _valueprobs(self, var, world):
            sums = [
             0] * var.valuecount()
            for gf in self.infer.var2gf[var.idx]:
                possible_values = []
                for i, value in var.itervalues(self.infer.mrf.evidence):
                    possible_values.append(i)
                    world_ = var.setval(value, list(world))
                    truth = gf(world_)
                    if truth == 0 and gf.ishard:
                        sums[i] = None
                    elif sums[i] is not None and not gf.ishard:
                        sums[i] += gf.weight * truth

                for i in [ j for j in range(len(sums)) if j not in possible_values ]:
                    sums[i] = None

            expsums = numpy.array([ numpy.exp(s) if s is not None else 0 for s in sums ])
            Z = sum(expsums)
            probs = expsums / Z
            return probs

        def step(self):
            mrf = self.infer.mrf
            state = list(self.state)
            for var in mrf.variables:
                values = list(var.values())
                if len(values) == 1:
                    continue
                probs = self._valueprobs(var, self.state)
                idx = None
                if idx is None:
                    r = random.uniform(0, 1)
                    idx = 0
                    s = probs[0]
                    while r > s:
                        idx += 1
                        s += probs[idx]

                var.setval(values[idx], self.state)

            self.update(self.state)
            return

    def _run(self, **params):
        """
        infer one or more probabilities P(F1 | F2)
        what: a ground formula (string) or a list of ground formulas (list of strings) (F1)
        given: a formula as a string (F2)
        set evidence according to given conjunction (if any)
        """
        chains = MCMCInference.ChainGroup(self)
        for i in range(self.chains):
            chain = GibbsSampler.Chain(self, self.queries)
            chains.chain(chain)

        converged = 0
        steps = 0
        if self.verbose:
            bar = ProgressBar(color='green', steps=self.maxsteps)
        while converged != self.chains and steps < self.maxsteps:
            converged = 0
            steps += 1
            for chain in chains.chains:
                chain.step()

            if self.verbose:
                bar.inc()
                bar.label('%d / %d' % (steps, self.maxsteps))

        return chains.results()[0]