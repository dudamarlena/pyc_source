# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nyga/code/pracmln/python2/pracmln/mln/inference/wcspinfer.py
# Compiled at: 2018-05-31 07:04:03
from dnutils import logs, out
from pracmln.mln.util import combinations, dict_union, Interval, temporary_evidence
from pracmln.mln.inference.infer import Inference
from pracmln.wcsp import Constraint
from pracmln.wcsp import WCSP
from pracmln.logic.common import Logic
from pracmln.mln.mrfvars import FuzzyVariable
from collections import defaultdict
from pracmln.mln.constants import infty, HARD
from pracmln.mln.grounding.fastconj import FastConjunctionGrounding
from pracmln.mln.grounding.default import DefaultGroundingFactory
from pracmln.mln.errors import SatisfiabilityException, MRFValueException
logger = logs.getlogger(__name__)

class WCSPInference(Inference):

    def __init__(self, mrf, queries, **params):
        Inference.__init__(self, mrf, queries, **params)

    def _run(self):
        result_ = {}
        with temporary_evidence(self.mrf):
            self.converter = WCSPConverter(self.mrf, multicore=self.multicore, verbose=self.verbose)
            result = self.result_dict(verbose=self.verbose)
            for query in self.queries:
                query = str(query)
                result_[query] = result[query] if query in result else self.mrf[query]

        return result_

    def result_dict(self, verbose=False):
        """
        Returns a Database object with the most probable truth assignment.
        """
        wcsp = self.converter.convert()
        solution, _ = wcsp.solve()
        if solution is None:
            raise Exception('MLN is unsatisfiable.')
        result = {}
        for varidx, validx in enumerate(solution):
            value = self.converter.domains[varidx][validx]
            result.update(self.converter.variables[varidx].value2dict(value))

        return dict([ (str(self.mrf.gndatom(idx)), val) for idx, val in result.iteritems() ])


class WCSPConverter(object):
    """
    Class for converting an MLN into a WCSP problem for efficient
    MPE inference.
    """

    def __init__(self, mrf, verbose=False, multicore=False):
        self.mrf = mrf
        self.constraints = {}
        self.verbose = verbose
        self._createvars()
        self.wcsp = WCSP()
        self.wcsp.domsizes = [ len(self.domains[i]) for i in self.variables ]
        self.multicore = multicore
        self._weights = None
        return

    def _createvars(self):
        """
        Create the variables, one binary for each ground atom.
        Considers also mutually exclusive blocks of ground atoms.
        """
        self.variables = {}
        self.domains = defaultdict(list)
        self.atom2var = {}
        self.val2idx = defaultdict(dict)
        varidx = 0
        for variable in self.mrf.variables:
            if isinstance(variable, FuzzyVariable):
                continue
            if variable.valuecount(self.mrf.evidence_dicti()) == 1:
                for _, value in variable.itervalues(self.mrf.evidence_dicti()):
                    break

                self.mrf.set_evidence(variable.value2dict(value), erase=False)
                continue
            self.variables[varidx] = variable
            for gndatom in variable.gndatoms:
                self.atom2var[gndatom.idx] = varidx

            for validx, (_, value) in enumerate(variable.itervalues(self.mrf.evidence_dicti())):
                self.domains[varidx].append(value)
                self.val2idx[varidx][value] = validx

            varidx += 1

    def convert(self):
        """
        Performs a conversion from an MLN into a WCSP.
        """
        self._weights = list(self.mrf.mln.weights)
        mln = self.mrf.mln
        logic = mln.logic
        formulas = []
        for f in self.mrf.formulas:
            if f.weight == 0:
                continue
            if f.weight < 0:
                f = logic.negate(f)
                f.weight = -f.weight
            if not any([ isinstance(c, logic.Exist) for c in f.constituents() ]):
                f = f.nnf()
            formulas.append(f)

        grounder = FastConjunctionGrounding(self.mrf, simplify=True, unsatfailure=True, formulas=formulas, multicore=self.multicore, verbose=self.verbose, cache=0)
        for gf in grounder.itergroundings():
            if isinstance(gf, Logic.TrueFalse):
                if gf.weight == HARD and gf.truth() == 0:
                    raise SatisfiabilityException('MLN is unsatisfiable: hard constraint %s violated' % self.mrf.mln.formulas[gf.idx])
                else:
                    continue
            self.generate_constraint(gf)

        self.mrf.mln.weights = self._weights
        return self.wcsp

    def generate_constraint(self, wf):
        """
        Generates and adds a constraint from a given weighted formula.
        """
        varindices = tuple(map(lambda x: self.atom2var[x], wf.gndatom_indices()))
        cost2assignments = self._gather_constraint_tuples(varindices, wf)
        if cost2assignments is None:
            return
        else:
            defcost = max(cost2assignments, key=lambda x: infty if cost2assignments[x] == 'else' else len(cost2assignments[x]))
            del cost2assignments[defcost]
            constraint = Constraint(varindices, defcost=defcost)
            for cost, tuples in cost2assignments.iteritems():
                for t in tuples:
                    constraint.tuple(t, cost)

            self.wcsp.constraint(constraint)
            return

    def _gather_constraint_tuples(self, varindices, formula):
        """
        Collects and evaluates all tuples that belong to the constraint
        given by a formula. In case of disjunctions and conjunctions,
        this is fairly efficient since not all combinations
        need to be evaluated. Returns a dictionary mapping the constraint
        costs to the list of respective variable assignments.
        """
        logic = self.mrf.mln.logic
        default_procedure = False
        conj = logic.islitconj(formula)
        disj = False
        if not conj:
            disj = logic.isclause(formula)
        if not varindices:
            return
        else:
            if not conj and not disj:
                default_procedure = True
            if not default_procedure:
                assignment = [
                 None] * len(varindices)
                children = list(formula.literals())
                for gndlit in children:
                    if isinstance(gndlit, Logic.TrueFalse):
                        continue
                    gndatom, val = gndlit.gndatom, not gndlit.negated
                    if disj:
                        val = not val
                    val = 1 if val else 0
                    variable = self.variables[self.atom2var[gndatom.idx]]
                    tmp_evidence = variable.value2dict(variable.evidence_value())
                    evval = tmp_evidence.get(gndatom.idx)
                    if evval is not None and evval != val:
                        return
                    tmp_evidence = dict_union(tmp_evidence, {gndatom.idx: val})
                    if variable.valuecount(tmp_evidence) > 1:
                        default_procedure = True
                        break
                    for _, value in variable.itervalues(tmp_evidence):
                        varidx = self.atom2var[gndatom.idx]
                        validx = self.val2idx[varidx][value]

                    if assignment[varindices.index(varidx)] is not None and assignment[varindices.index(varidx)] != value:
                        if formula.weight == HARD:
                            if conj:
                                raise SatisfiabilityException('Knowledge base is unsatisfiable due to hard constraint violation: %s' % formula)
                            elif disj:
                                continue
                        else:
                            return
                    assignment[varindices.index(varidx)] = validx

                if not default_procedure:
                    maxtruth = formula.maxtruth(self.mrf.evidence)
                    mintruth = formula.mintruth(self.mrf.evidence)
                    if formula.weight == HARD and (maxtruth in Interval(']0,1[') or mintruth in Interval(']0,1[')):
                        raise MRFValueException('No fuzzy truth values are allowed in hard constraints.')
                    if conj:
                        if formula.weight == HARD:
                            cost = 0
                            defcost = self.wcsp.top
                        else:
                            cost = formula.weight * (1 - maxtruth)
                            defcost = formula.weight
                    elif formula.weight == HARD:
                        cost = self.wcsp.top
                        defcost = 0
                    else:
                        defcost = 0
                        cost = formula.weight * (1 - mintruth)
                    if len(assignment) != len(varindices):
                        raise MRFValueException('Illegal variable assignments. Variables: %s, Assignment: %s' % (varindices, assignment))
                    return {cost: [tuple(assignment)], defcost: 'else'}
            if default_procedure:
                domains = [ self.domains[v] for v in varindices ]
                cost2assignments = defaultdict(list)
                worlds = 1
                for d in domains:
                    worlds *= len(d)

                if worlds > 1000000:
                    logger.warning('!!! WARNING: %d POSSIBLE WORLDS ARE GOING TO BE EVALUATED. KEEP IN SIGHT YOUR MEMORY CONSUMPTION !!!' % worlds)
                for c in combinations(domains):
                    world = [
                     0] * len(self.mrf.gndatoms)
                    assignment = []
                    for varidx, value in zip(varindices, c):
                        world = self.variables[varidx].setval(value, world)
                        assignment.append(self.val2idx[varidx][value])

                    truth = formula(world)
                    if truth is None:
                        print 'POSSIBLE WORLD:'
                        print '==============='
                        self.mrf.print_world_vars(world)
                        print 'GROUND FORMULA:'
                        print '==============='
                        formula.print_structure(world)
                        raise Exception('Something went wrong: Truth of ground formula cannot be evaluated (see above)')
                    if truth in Interval(']0,1[') and formula.weight == HARD:
                        raise MRFValueException('No fuzzy truth values are allowed in hard constraints.')
                    if formula.weight == HARD:
                        if truth == 1:
                            cost = 0
                        else:
                            cost = self.wcsp.top
                    else:
                        cost = (1 - truth) * formula.weight
                    cost2assignments[cost].append(tuple(assignment))

                return cost2assignments
            assert False
            return

    def forbid_gndatom(self, atom, truth=True):
        """
        Adds a unary constraint that prohibits the given ground atom
        being true.
        """
        atomidx = atom if type(atom) is int else self.mrf.gndatom(atom).idx if type(atom) is str else atom.idx
        varidx = self.atom2var[atomidx]
        variable = self.variables[varidx]
        evidence = list(self.mrf.evidence)
        evidence[atomidx] = {True: 1, False: 0}[truth]
        c = Constraint((varidx,))
        for _, value in variable.itervalues(evidence):
            validx = self.val2idx[varidx][value]
            c.tuple((validx,), self.wcsp.top)

        self.wcsp.constraint(c)

    def getPseudoDistributionForGndAtom(self, gndAtom):
        """
        Computes a relative "distribution" for all possible variable assignments of 
        a mutex constraint. This can be used to determine the confidence in particular
        most probable world by comparing the score with the second-most probable one.
        """
        if isinstance(gndAtom, basestring):
            gndAtom = self.mrf.gndAtoms[gndAtom]
        if not isinstance(gndAtom, Logic.GroundAtom):
            raise Exception('Argument must be a ground atom')
        varIdx = self.gndAtom2VarIndex[gndAtom]
        valIndices = range(len(self.varIdx2GndAtom[varIdx]))
        mutex = len(self.varIdx2GndAtom[varIdx]) > 1
        if not mutex:
            raise Exception('Pseudo distribution is provided for mutex constraints only.')
        wcsp = self.convert()
        atoms = []
        cost = []
        try:
            while len(valIndices) > 0:
                s, c = wcsp.solve()
                if s is None:
                    raise Exception()
                val = s[varIdx]
                atom = self.varIdx2GndAtom[varIdx][val]
                self.forbidGndAtom(atom, wcsp)
                valIndices.remove(val)
                cost.append(c)
                atoms.append(atom)

        except:
            pass

        c_max = max(cost)
        for i, c in enumerate(cost):
            cost[i] = c_max - c

        c_sum = sum(cost)
        for i, c in enumerate(cost):
            cost[i] = float(c) / c_sum

        return dict([ (a, c) for a, c in zip(atoms, cost) ])


if __name__ == '__main__':
    pass