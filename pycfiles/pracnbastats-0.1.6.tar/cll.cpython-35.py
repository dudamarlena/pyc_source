# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nyga/work/code/pracmln/python3/pracmln/mln/learning/cll.py
# Compiled at: 2018-04-24 04:48:32
# Size of source mod 2**32: 17653 bytes
from dnutils import logs
from .common import AbstractLearner, DiscriminativeLearner
import random
from collections import defaultdict
from ..util import fsum, dict_union, temporary_evidence
from numpy.ma.core import log, sqrt
import numpy
from ...logic.common import Logic
from ..constants import HARD
from ..errors import SatisfiabilityException
logger = logs.getlogger(__name__)

class CLL(AbstractLearner):
    """CLL"""

    def __init__(self, mrf, **params):
        AbstractLearner.__init__(self, mrf, **params)
        self.partitions = []
        self.repart = 0

    @property
    def partsize(self):
        return self._params.get('partsize', 1)

    @property
    def maxiter(self):
        return self._params.get('maxiter', 10)

    @property
    def variables(self):
        return self.mrf.variables

    def _prepare(self):
        self.partitions = []
        self.atomidx2partition = {}
        self.partition2formulas = defaultdict(set)
        self.evidx = {}
        self.valuecounts = {}
        self.partitionProbValues = {}
        self.current_wts = None
        self.iter = 0
        self.probs = {}
        self._stat = {}
        size = self.partsize
        variables = list(self.variables)
        if size > 1:
            random.shuffle(variables)
        while len(variables) > 0:
            vars_ = variables[:size if len(variables) > size else len(variables)]
            partidx = len(self.partitions)
            partition = CLL.Partition(self.mrf, vars_, partidx)
            for atom in partition.gndatoms:
                self.atomidx2partition[atom.idx] = partition

            logger.debug('created partition: %s' % str(partition))
            self.valuecounts[partidx] = partition.valuecount()
            self.partitions.append(partition)
            self.evidx[partidx] = partition.evidenceidx()
            variables = variables[len(partition.variables):]

        logger.debug('CLL created %d partitions' % len(self.partitions))
        self._compute_statistics()

    def repeat(self):
        return True

    def _addstat(self, fidx, pidx, validx, inc=1):
        if fidx not in self._stat:
            self._stat[fidx] = {}
        d = self._stat[fidx]
        if pidx not in d:
            d[pidx] = [
             0] * self.valuecounts[pidx]
        try:
            d[pidx][validx] += inc
        except Exception as e:
            raise e

    def _compute_statistics(self):
        self._stat = {}
        self.partition2formulas = defaultdict(set)
        for formula in self.mrf.formulas:
            literals = []
            for lit in formula.literals():
                literals.append(lit)

            isconj = self.mrf.mln.logic.islitconj(formula)
            if isconj:
                literals = sorted(literals, key=lambda l: -1 if isinstance(l, Logic.Equality) else 1)
            self._compute_stat_rec(literals, [], {}, formula, isconj=isconj)

    def _compute_stat_rec(self, literals, gndliterals, var_assign, formula, f_gndlit_parts=None, processed=None, isconj=False):
        """
        TODO: make sure that there are no equality constraints in the conjunction!
        """
        if len(literals) == 0:
            part2gndlits = defaultdict(list)
            part_with_f_lit = None
            for gndlit in gndliterals:
                if not isinstance(gndlit, Logic.Equality):
                    if hasattr(self, 'qpreds') and gndlit.gndatom.predname not in self.qpreds:
                        pass
                    else:
                        part = self.atomidx2partition[gndlit.gndatom.idx]
                        part2gndlits[part].append(gndlit)
                        if gndlit(self.mrf.evidence) == 0:
                            part_with_f_lit = part

            if isconj and part_with_f_lit is not None:
                gndlits = part2gndlits[part_with_f_lit]
                part2gndlits = {part_with_f_lit: gndlits}
            if not isconj:
                gndformula = formula.ground(self.mrf, var_assign)
            for partition, gndlits in part2gndlits.items():
                evidence = {}
                if isconj:
                    for gndlit in gndlits:
                        evidence[gndlit.gndatom.idx] = 0 if gndlit.negated else 1

                for world in partition.itervalues(evidence):
                    worldidx = partition.valueidx(world)
                    if isconj:
                        truth = 1
                    else:
                        with temporary_evidence(self.mrf):
                            for atomidx, value in partition.value2dict(world).items():
                                self.mrf.set_evidence({atomidx: value}, erase=True)

                            truth = gndformula(self.mrf.evidence)
                            if truth is None:
                                print(gndformula)
                                print(gndformula.print_structure(self.mrf.evidence))
                    if truth != 0:
                        self.partition2formulas[partition.idx].add(formula.idx)
                        self._addstat(formula.idx, partition.idx, worldidx, truth)

            return
        lit = literals[0]
        gndlit = lit.ground(self.mrf, var_assign, partial=True)
        for assign in Logic.iter_eq_varassignments(gndlit, formula, self.mrf) if isinstance(gndlit, Logic.Equality) else gndlit.itervargroundings(self.mrf):
            if processed is None:
                processed = []
            else:
                processed = list(processed)
            gndlit_ = gndlit.ground(self.mrf, assign)
            truth = gndlit_(self.mrf.evidence)
            if isinstance(gndlit_, Logic.Equality):
                if isconj:
                    if truth == 1:
                        self._compute_stat_rec(literals[1:], gndliterals, dict_union(var_assign, assign), formula, f_gndlit_parts, processed, isconj)
                    else:
                        continue
                else:
                    self._compute_stat_rec(literals[1:], gndliterals + [gndlit_], dict_union(var_assign, assign), formula, f_gndlit_parts, processed, isconj)
                    continue
                    atom = gndlit_.gndatom
                    if atom.idx in processed:
                        pass
                    else:
                        isevidence = hasattr(self, 'qpreds') and gndlit_.gndatom.predname not in self.qpreds
                        if isconj and truth == 0:
                            if f_gndlit_parts is not None and atom not in f_gndlit_parts:
                                continue
                            elif isevidence:
                                pass
                        else:
                            self._compute_stat_rec(literals[1:], gndliterals + [gndlit_], dict_union(var_assign, assign), formula, self.atomidx2partition[atom.idx], processed, isconj)
                            continue
            elif isconj and isevidence:
                self._compute_stat_rec(literals[1:], gndliterals, dict_union(var_assign, assign), formula, f_gndlit_parts, processed, isconj)
                continue
            self._compute_stat_rec(literals[1:], gndliterals + [gndlit_], dict_union(var_assign, assign), formula, f_gndlit_parts, processed, isconj)

    def _compute_probs(self, w):
        probs = {}
        for pidx in range(len(self.partitions)):
            expsums = [0] * self.valuecounts[pidx]
            for fidx in self.partition2formulas[pidx]:
                for i, v in enumerate(self._stat[fidx][pidx]):
                    if w[fidx] == HARD:
                        if v == 0:
                            expsums[i] = None
                        else:
                            if expsums[i] is not None:
                                expsums[i] += v * w[fidx]

            expsum = numpy.array([numpy.exp(s) if s is not None else 0 for s in expsums])
            z = fsum(expsum)
            if z == 0:
                raise SatisfiabilityException('MLN is unsatisfiable: all probability masses of partition %s are zero.' % str(self.partitions[pidx]))
            probs[pidx] = expsum / z
            self.probs[pidx] = expsum

        self.probs = probs
        return probs

    def _f(self, w):
        if self.current_wts is None or list(w) != self.current_wts:
            self.current_wts = list(w)
            self.probs = self._compute_probs(w)
        likelihood = numpy.zeros(len(self.partitions))
        for pidx in range(len(self.partitions)):
            p = self.probs[pidx][self.evidx[pidx]]
            if p == 0:
                p = 1e-10
            likelihood[pidx] += p

        self.iter += 1
        return fsum(list(map(log, likelihood)))

    def _grad(self, w, **params):
        if self.current_wts is None or not list(w) != self.current_wts:
            self.current_wts = w
            self.probs = self._compute_probs(w)
        grad = numpy.zeros(len(w))
        for fidx, partitions in self._stat.items():
            for part, values in partitions.items():
                v = values[self.evidx[part]]
                for i, val in enumerate(values):
                    v -= self.probs[part][i] * val

                grad[fidx] += v

        self.grad_opt_norm = sqrt(float(fsum([x * x for x in grad])))
        return numpy.array(grad)

    class Partition(object):
        """CLL.Partition"""

        def __init__(self, mrf, variables, idx):
            self.variables = variables
            self.mrf = mrf
            self.idx = idx

        @property
        def gndatoms(self):
            atoms = []
            for v in self.variables:
                atoms.extend(v.gndatoms)

            return atoms

        def __contains__(self, atom):
            """
            Returns True iff the given ground atom or ground atom index is part of
            this partition.
            """
            if isinstance(atom, Logic.GroundAtom):
                return atom in self.gndatoms
            if type(atom) is int:
                return self.mrf.gndatom(atom) in self
            raise Exception('Invalid type of atom: %s' % type(atom))

        def value2dict(self, value):
            """
            Takes a possible world tuple of the form ((0,),(0,),(1,0,0),(1,)) and transforms
            it into a dict mapping the respective atom indices to their truth values
            """
            evidence = {}
            for var, val in zip(self.variables, value):
                evidence.update(var.value2dict(val))

            return evidence

        def evidenceidx(self, evidence=None):
            """
            Returns the index of the possible world value of this partition that is represented
            by evidence. If evidence is None, the evidence set in the MRF is used.
            """
            if evidence is None:
                evidence = self.mrf.evidence
            evidencevalue = []
            for var in self.variables:
                evidencevalue.append(var.evidence_value(evidence))

            return self.valueidx(tuple(evidencevalue))

        def valueidx(self, value):
            """
            Computes the index of the given possible world that would be assigned
            to it by recursively generating all worlds by itervalues().
            value needs to be represented by a (nested) tuple of truth values.
            Exp: ((0,),(0,),(1,0,0),(0,)) --> 0
                 ((0,),(0,),(1,0,0),(1,)) --> 1
                 ((0,),(0,),(0,1,0),(0,)) --> 2
                 ((0,),(0,),(0,1,0),(1,)) --> 3
                 ...
            """
            idx = 0
            for i, (var, val) in enumerate(zip(self.variables, value)):
                exponential = 2 ** (len(self.variables) - i - 1)
                validx = var.valueidx(val)
                idx += validx * exponential

            return idx

        def itervalues(self, evidence=None):
            """
            Yields possible world values of this partition in the form
            ((0,),(0,),(1,0,0),(0,)), for instance. Nested tuples represent mutex variables.
            All tuples are consistent with the evidence at hand. Evidence is
            a dict mapping a ground atom index to its (binary) truth value.
            """
            if evidence is None:
                evidence = []
            for world in self._itervalues(self.variables, [], evidence):
                yield world

        def _itervalues(self, variables, assignment, evidence):
            """
            Recursively generates all tuples of possible worlds that are consistent
            with the evidence at hand.
            """
            if not variables:
                yield tuple(assignment)
                return
            var = variables[0]
            for _, val in var.itervalues(evidence):
                for world in self._itervalues(variables[1:], assignment + [val], evidence):
                    yield world

        def valuecount(self):
            """
            Returns the number of possible (partial) worlds of this partition
            """
            count = 1
            for v in self.variables:
                count *= v.valuecount()

            return count

        def __str__(self):
            s = []
            for v in self.variables:
                s.append(str(v))

            return '%d: [%s]' % (self.idx, ','.join(s))


class DCLL(CLL, DiscriminativeLearner):
    """DCLL"""

    def __init__(self, mrf=None, **params):
        CLL.__init__(self, mrf, **params)

    @property
    def variables(self):
        return [var for var in self.mrf.variables if var.predicate.name in self.qpreds]


Partition = CLL.Partition