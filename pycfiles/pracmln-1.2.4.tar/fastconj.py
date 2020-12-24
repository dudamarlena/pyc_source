# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python2/pracmln/mln/grounding/fastconj.py
# Compiled at: 2018-04-24 04:48:32
from dnutils import logs, ProgressBar
from pracmln.mln.grounding.default import DefaultGroundingFactory
from pracmln.logic.common import Logic
import types
from multiprocessing.pool import Pool
from pracmln.utils.multicore import with_tracing
from itertools import imap
from pracmln.mln.mlnpreds import FunctionalPredicate, SoftFunctionalPredicate, FuzzyPredicate
from pracmln.mln.util import dict_union, rndbatches, cumsum
from pracmln.mln.errors import SatisfiabilityException
from pracmln.mln.constants import HARD
from collections import defaultdict
from pracmln.logic.fuzzy import FuzzyLogic
logger = logs.getlogger(__name__)
global_fastConjGrounding = None

def create_formula_groundings(formulas):
    global global_fastConjGrounding
    gfs = []
    for formula in sorted(formulas, key=global_fastConjGrounding._fsort):
        if global_fastConjGrounding.mrf.mln.logic.islitconj(formula) or global_fastConjGrounding.mrf.mln.logic.isclause(formula):
            for gf in global_fastConjGrounding.itergroundings_fast(formula):
                gfs.append(gf)

        else:
            for gf in formula.itergroundings(global_fastConjGrounding.mrf, simplify=True):
                gfs.append(gf)

    return gfs


class FastConjunctionGrounding(DefaultGroundingFactory):
    """
    Fairly fast grounding of conjunctions pruning the grounding tree if a
    formula is rendered false by the evidence. Performs some heuristic
    sorting such that equality constraints are evaluated first.
    """

    def __init__(self, mrf, simplify=False, unsatfailure=False, formulas=None, cache=None, **params):
        DefaultGroundingFactory.__init__(self, mrf, simplify=simplify, unsatfailure=unsatfailure, formulas=formulas, cache=cache, **params)

    def _conjsort(self, e):
        if isinstance(e, Logic.Equality):
            return 0.5
        else:
            if isinstance(e, Logic.TrueFalse):
                return 1
            if isinstance(e, Logic.GroundLit):
                if self.mrf.evidence[e.gndatom.idx] is not None:
                    return 2
                else:
                    if type(self.mrf.mln.predicate(e.gndatom.predname)) in (FunctionalPredicate, SoftFunctionalPredicate):
                        return 3
                    return 4

            else:
                if isinstance(e, Logic.Lit) and type(self.mrf.mln.predicate(e.predname)) in (FunctionalPredicate, SoftFunctionalPredicate, FuzzyPredicate):
                    return 5
                else:
                    if isinstance(e, Logic.Lit):
                        return 6
                    return 7

            return

    @staticmethod
    def _fsort(f):
        if f.weight == HARD:
            return 0
        else:
            return 1

    def itergroundings_fast(self, formula):
        """
        Recursively generate the groundings of a conjunction that do _not_
        have a definite truth value yet given the evidence.
        """
        formula = formula.ground(self.mrf, {}, partial=True, simplify=True)
        children = [hasattr(formula, 'children') or formula] if 1 else formula.children
        variables = formula.vardoms()

        def eqvardoms(self, v=None, c=None):
            if v is None:
                v = defaultdict(set)
            for a in self.args:
                if self.mln.logic.isvar(a):
                    v[a] = variables[a]

            return v

        for child in children:
            if isinstance(child, Logic.Equality):
                setattr(child, 'vardoms', types.MethodType(eqvardoms, child))

        lits = sorted(children, key=self._conjsort)
        truthpivot, pivotfct = (1, FuzzyLogic.min_undef) if isinstance(formula, Logic.Conjunction) else (0, FuzzyLogic.max_undef) if isinstance(formula, Logic.Disjunction) else (None,
                                                                                                                                                                                  None)
        for gf in self._itergroundings_fast(formula, lits, 0, pivotfct, truthpivot, {}):
            yield gf

        return

    def _itergroundings_fast(self, formula, constituents, cidx, pivotfct, truthpivot, assignment, level=0):
        if truthpivot == 0 and (isinstance(formula, Logic.Conjunction) or self.mrf.mln.logic.islit(formula)):
            if formula.weight == HARD:
                raise SatisfiabilityException(('MLN is unsatisfiable given evidence due to hard constraint violation: {}').format(str(formula)))
            return
        if truthpivot == 1 and (isinstance(formula, Logic.Disjunction) or self.mrf.mln.logic.islit(formula)):
            return
        if cidx == len(constituents):
            gf = formula.ground(self.mrf, assignment, simplify=True)
            if isinstance(gf, Logic.TrueFalse):
                return
            yield gf
            return
        else:
            c = constituents[cidx]
            for varass in c.itervargroundings(self.mrf, partial=assignment):
                newass = dict_union(assignment, varass)
                ga = c.ground(self.mrf, newass)
                truth = ga.truth(self.mrf.evidence)
                if truth is None:
                    truthpivot_ = truthpivot
                else:
                    if truthpivot is None:
                        truthpivot_ = truth
                    else:
                        truthpivot_ = pivotfct(truthpivot, truth)
                    for gf in self._itergroundings_fast(formula, constituents, cidx + 1, pivotfct, truthpivot_, newass, level + 1):
                        yield gf

            return

    def _itergroundings(self, simplify=True, unsatfailure=True):
        global global_fastConjGrounding
        if not self.formulas:
            return
        global_fastConjGrounding = self
        batches = list(rndbatches(self.formulas, 20))
        batchsizes = [ len(b) for b in batches ]
        if self.verbose:
            bar = ProgressBar(steps=sum(batchsizes), color='green')
            i = 0
        if self.multicore:
            pool = Pool()
            try:
                try:
                    for gfs in pool.imap(with_tracing(create_formula_groundings), batches):
                        if self.verbose:
                            bar.inc(batchsizes[i])
                            bar.label(str(cumsum(batchsizes, i + 1)))
                            i += 1
                        for gf in gfs:
                            yield gf

                except Exception as e:
                    logger.error('Error in child process. Terminating pool...')
                    pool.close()
                    raise e

            finally:
                pool.terminate()
                pool.join()

        else:
            for gfs in imap(create_formula_groundings, batches):
                if self.verbose:
                    bar.inc(batchsizes[i])
                    bar.label(str(cumsum(batchsizes, i + 1)))
                    i += 1
                for gf in gfs:
                    yield gf