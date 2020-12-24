# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python2/pracmln/mln/inference/mcmc.py
# Compiled at: 2018-04-24 04:48:32
import random
from dnutils import logs
from pracmln.mln.inference.infer import Inference
from pracmln.mln.util import fstr
from pracmln.mln.constants import ALL
logger = logs.getlogger(__name__)

class MCMCInference(Inference):
    """
    Abstract super class for Markov chain Monte Carlo-based inference.
    """

    def __init__(self, mrf, queries=ALL, **params):
        Inference.__init__(self, mrf, queries, **params)

    def random_world(self, evidence=None):
        """
        Get a random possible world, taking the evidence into account.
        """
        if evidence is None:
            world = list(self.mrf.evidence)
        else:
            world = list(evidence)
        for var in self.mrf.variables:
            evdict = var.value2dict(var.evidence_value(world))
            valuecount = var.valuecount(evdict)
            if valuecount > 1:
                validx = random.randint(0, valuecount - 1)
                value = [ v for _, v in var.itervalues(evdict) ][validx]
                var.setval(value, world)

        return world

    class Chain:
        """
        Represents the state of a Markov Chain.
        """

        def __init__(self, infer, queries):
            self.queries = queries
            self.soft_evidence = None
            self.steps = 0
            self.truths = [0] * len(self.queries)
            self.converged = False
            self.lastresult = 10
            self.infer = infer
            self.state = infer.random_world()
            return

        def update(self, state):
            self.steps += 1
            self.state = state
            for i, q in enumerate(self.queries):
                self.truths[i] += q(self.state)

            if self.steps % 50 == 0:
                result = self.results()[0]
                diff = abs(result - self.lastresult)
                if diff < 0.001:
                    self.converged = True
                self.lastresult = result
            if self.soft_evidence is not None:
                for se in self.soft_evidence:
                    self.softev_counts[se['expr']] += se['formula'](self.state)

            return

        def set_soft_evidence(self, soft_evidence):
            self.soft_evidence = soft_evidence
            self.softev_counts = {}
            for se in soft_evidence:
                if 'formula' not in se:
                    formula = self.infer.mrf.mln.logic.parse_formula(se['expr'])
                    se['formula'] = formula.ground(self.infer.mrf, {})
                    se['expr'] = fstr(se['formula'])
                self.softev_counts[se['expr']] = se['formula'](self.state)

        def soft_evidence_frequency(self, formula):
            if self.steps == 0:
                return 0
            return float(self.softev_counts[fstr(formula)]) / self.steps

        def results(self):
            results = []
            for i in range(len(self.queries)):
                results.append(float(self.truths[i]) / self.steps)

            return results

    class ChainGroup:

        def __init__(self, infer):
            self.chains = []
            self.infer = infer

        def chain(self, chain):
            self.chains.append(chain)

        def results(self):
            chains = float(len(self.chains))
            queries = self.chains[0].queries
            results = [
             0.0] * len(queries)
            for chain in self.chains:
                cr = chain.results()
                for i in range(len(queries)):
                    results[i] += cr[i] / chains

            var = [ 0.0 for i in range(len(queries)) ]
            for chain in self.chains:
                cr = chain.results()
                for i in range(len(self.chains[0].queries)):
                    var[i] += (cr[i] - results[i]) ** 2 / chains

            return (
             dict([ (str(q), p) for q, p in zip(queries, results) ]), var)

        def avgtruth(self, formula):
            """ returns the fraction of chains in which the given formula is currently true """
            t = 0.0
            for c in self.chains:
                t += formula(c.state)

            return t / len(self.chains)