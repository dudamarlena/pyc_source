# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python3/pracmln/mln/inference/exact.py
# Compiled at: 2018-04-24 04:48:32
# Size of source mod 2**32: 7541 bytes
from dnutils import logs, ProgressBar
from .infer import Inference
from multiprocessing import Pool
from ..mrfvars import FuzzyVariable
from ..constants import auto, HARD
from ..errors import SatisfiabilityException
from ..grounding.fastconj import FastConjunctionGrounding
from ..util import Interval, colorize
from ...utils.multicore import with_tracing
from ...logic.fol import FirstOrderLogic
from ...logic.common import Logic
from numpy.ma.core import exp
logger = logs.getlogger(__name__)
global_enumAsk = None

def eval_queries(world):
    """
    Evaluates the queries given a possible world.
    """
    global global_enumAsk
    numerators = [
     0] * len(global_enumAsk.queries)
    denominator = 0
    expsum = 0
    for gf in global_enumAsk.grounder.itergroundings():
        if global_enumAsk.soft_evidence_formula(gf):
            expsum += gf.noisyor(world) * gf.weight
        else:
            truth = gf(world)
            if gf.weight == HARD:
                if truth in Interval(']0,1['):
                    raise Exception('No real-valued degrees of truth are allowed in hard constraints.')
                if truth == 1:
                    continue
                else:
                    return (
                     numerators, 0)
                expsum += gf(world) * gf.weight

    expsum = exp(expsum)
    for i, query in enumerate(global_enumAsk.queries):
        if query(world):
            numerators[i] += expsum

    denominator += expsum
    return (numerators, denominator)


class EnumerationAsk(Inference):
    __doc__ = '\n    Inference based on enumeration of (only) the worlds compatible with the\n    evidence; supports soft evidence (assuming independence)\n    '

    def __init__(self, mrf, queries, **params):
        Inference.__init__(self, mrf, queries, **params)
        self.grounder = FastConjunctionGrounding(mrf, simplify=False, unsatfailure=False, formulas=mrf.formulas, cache=auto, verbose=False, multicore=False)
        for variable in self.mrf.variables:
            variable.consistent(self.mrf.evidence, strict=isinstance(variable, FuzzyVariable))

    def _run(self):
        """
        verbose: whether to print results (or anything at all, in fact)
        details: (given that verbose is true) whether to output additional
                 status information
        debug:   (given that verbose is true) if true, outputs debug
                 information, in particular the distribution over possible
                 worlds
        debugLevel: level of detail for debug mode
        """
        global global_enumAsk
        self._watch.tag('check hard constraints', verbose=self.verbose)
        hcgrounder = FastConjunctionGrounding(self.mrf, simplify=False, unsatfailure=True, formulas=[f for f in self.mrf.formulas if f.weight == HARD], **self._params + {'multicore': False, 'verbose': False})
        for gf in hcgrounder.itergroundings():
            if isinstance(gf, Logic.TrueFalse) and gf.truth() == 0.0:
                raise SatisfiabilityException('MLN is unsatisfiable due to hard constraint violation by evidence: {} ({})'.format(str(gf), str(self.mln.formula(gf.idx))))

        self._watch.finish('check hard constraints')
        worlds = 1
        for variable in self.mrf.variables:
            values = variable.valuecount(self.mrf.evidence)
            worlds *= values

        numerators = [0.0 for i in range(len(self.queries))]
        denominator = 0.0
        logger.debug('Summing over %d possible worlds...' % worlds)
        if worlds > 500000 and self.verbose:
            print(colorize('!!! %d WORLDS WILL BE ENUMERATED !!!' % worlds, (None,
                                                                             'red',
                                                                             True), True))
        k = 0
        self._watch.tag('enumerating worlds', verbose=self.verbose)
        global_enumAsk = self
        bar = None
        if self.verbose:
            bar = ProgressBar(steps=worlds, color='green')
        if self.multicore:
            pool = Pool()
            logger.debug('Using multiprocessing on {} core(s)...'.format(pool._processes))
            try:
                try:
                    for num, denum in pool.imap(with_tracing(eval_queries), self.mrf.worlds()):
                        denominator += denum
                        k += 1
                        for i, v in enumerate(num):
                            numerators[i] += v

                        if self.verbose:
                            bar.inc()

                except Exception as e:
                    logger.error('Error in child process. Terminating pool...')
                    pool.close()
                    raise e

            finally:
                pool.terminate()
                pool.join()

        else:
            for world in self.mrf.worlds():
                num, denom = eval_queries(world)
                denominator += denom
                for i, _ in enumerate(self.queries):
                    numerators[i] += num[i]

                k += 1
                if self.verbose:
                    bar.update(float(k) / worlds)

        logger.debug('%d worlds enumerated' % k)
        self._watch.finish('enumerating worlds')
        if 'grounding' in self.grounder.watch.tags:
            self._watch.tags['grounding'] = self.grounder.watch['grounding']
        if denominator == 0:
            raise SatisfiabilityException('MLN is unsatisfiable. All probability masses returned 0.')
        dist = [float(x) / denominator for x in numerators]
        result = {}
        for q, p in zip(self.queries, dist):
            result[str(q)] = p

        return result

    def soft_evidence_formula(self, gf):
        truths = [a.truth(self.mrf.evidence) for a in gf.gndatoms()]
        if None in truths:
            return False
        return isinstance(self.mrf.mln.logic, FirstOrderLogic) and any([t in Interval('(0,1)') for t in truths])