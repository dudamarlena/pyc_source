# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/code/pracmln/python3/pracmln/mln/inference/wcspinfer.py
# Compiled at: 2019-02-27 05:10:32
# Size of source mod 2**32: 16630 bytes
from collections import defaultdict
from dnutils import logs
from .infer import Inference
from ..constants import infty, HARD
from ..errors import SatisfiabilityException, MRFValueException
from ..grounding.fastconj import FastConjunctionGrounding
from ..mrfvars import FuzzyVariable
from ..util import combinations, dict_union, Interval, temporary_evidence
from ...wcsp import Constraint, WCSP
from ...logic.common import Logic
logger = logs.getlogger(__name__)

class WCSPInference(Inference):

    def __init__(self, mrf, queries, **params):
        (Inference.__init__)(self, mrf, queries, **params)

    def _run(self):
        result_ = {}
        with temporary_evidence(self.mrf):
            self.converter = WCSPConverter((self.mrf), multicore=(self.multicore), verbose=(self.verbose))
            result = self.result_dict(verbose=(self.verbose))
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

        return dict([(str(self.mrf.gndatom(idx)), val) for idx, val in result.items()])


class WCSPConverter(object):
    __doc__ = '\n    Class for converting an MLN into a WCSP problem for efficient\n    MPE inference.\n    '

    def __init__(self, mrf, verbose=False, multicore=False):
        self.mrf = mrf
        self.constraints = {}
        self.verbose = verbose
        self._createvars()
        self.wcsp = WCSP()
        self.wcsp.domsizes = [len(self.domains[i]) for i in self.variables]
        self.multicore = multicore

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

                self.mrf.set_evidence((variable.value2dict(value)), erase=False)
            else:
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
                pass
            else:
                if f.weight < 0:
                    f = logic.negate(f)
                    f.weight = -f.weight
                formulas.append(f.nnf())

        grounder = FastConjunctionGrounding((self.mrf), simplify=True, unsatfailure=True, formulas=formulas, multicore=(self.multicore), verbose=(self.verbose), cache=0)
        for gf in grounder.itergroundings():
            if isinstance(gf, Logic.TrueFalse):
                if gf.weight == HARD:
                    if gf.truth() == 0:
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
        varindices = tuple([self.atom2var[x] for x in wf.gndatom_indices()])
        seen = set()
        varindices_ = []
        for v in varindices:
            if v in seen:
                pass
            else:
                varindices_.append(v)
                seen.add(v)

        varindices = tuple(varindices_)
        cost2assignments = self._gather_constraint_tuples(varindices, wf)
        if cost2assignments is None:
            return
        defcost = max(cost2assignments, key=(lambda x: infty if cost2assignments[x] == 'else' else len(cost2assignments[x])))
        del cost2assignments[defcost]
        constraint = Constraint(varindices, defcost=defcost)
        for cost, tuples in cost2assignments.items():
            for t in tuples:
                constraint.tuple(t, cost)

        self.wcsp.constraint(constraint)

    def _gather_constraint_tuples(self, varindices, formula):
        """
        Collects and evaluates all tuples that belong to the constraint
        given by a formula. In case of disjunctions and conjunctions,
        this is fairly efficient since not all combinations
        need to be evaluated. Returns a dictionary mapping the constraint
        costs to the list of respective variable assignments.
        """
        logic = self.mrf.mln.logic
        defaultProcedure = False
        conj = logic.islitconj(formula)
        disj = False
        if not conj:
            disj = logic.isclause(formula)
        else:
            if not varindices:
                return
            else:
                if not conj:
                    if not disj:
                        defaultProcedure = True
                else:
                    if not defaultProcedure:
                        assignment = [
                         None] * len(varindices)
                        children = list(formula.literals())
                        for gndlit in children:
                            if isinstance(gndlit, Logic.TrueFalse):
                                pass
                            else:
                                gndatom, val = gndlit.gndatom, not gndlit.negated
                                if disj:
                                    val = not val
                                val = 1 if val else 0
                                variable = self.variables[self.atom2var[gndatom.idx]]
                                tmp_evidence = variable.value2dict(variable.evidence_value())
                                evval = tmp_evidence.get(gndatom.idx)
                                if evval is not None:
                                    if evval != val:
                                        return
                                tmp_evidence = dict_union(tmp_evidence, {gndatom.idx: val})
                                if variable.valuecount(tmp_evidence) > 1:
                                    defaultProcedure = True
                                    break
                                for _, value in variable.itervalues(tmp_evidence):
                                    varidx = self.atom2var[gndatom.idx]
                                    validx = self.val2idx[varidx][value]

                                if assignment[varindices.index(varidx)] is not None:
                                    if assignment[varindices.index(varidx)] != value:
                                        if formula.weight == HARD:
                                            if conj:
                                                raise SatisfiabilityException('Knowledge base is unsatisfiable due to hard constraint violation: %s' % formula)
                                            else:
                                                if disj:
                                                    continue
                                        else:
                                            return
                                assignment[varindices.index(varidx)] = validx

                        if not defaultProcedure:
                            maxtruth = formula.maxtruth(self.mrf.evidence)
                            mintruth = formula.mintruth(self.mrf.evidence)
                            if formula.weight == HARD:
                                if maxtruth in Interval(']0,1[') or mintruth in Interval(']0,1['):
                                    raise MRFValueException('No fuzzy truth values are allowed in hard constraints.')
                            if conj:
                                if formula.weight == HARD:
                                    cost = 0
                                    defcost = self.wcsp.top
                                else:
                                    cost = formula.weight * (1 - maxtruth)
                                    defcost = formula.weight
                            else:
                                if formula.weight == HARD:
                                    cost = self.wcsp.top
                                    defcost = 0
                                else:
                                    defcost = 0
                                    cost = formula.weight * (1 - mintruth)
                                if len(assignment) != len(varindices):
                                    raise MRFValueException('Illegal variable assignments. Variables: %s, Assignment: %s' % (varindices, assignment))
                                return {cost: [tuple(assignment)], defcost: 'else'}
                if defaultProcedure:
                    domains = [self.domains[v] for v in varindices]
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
                            print('POSSIBLE WORLD:')
                            print('===============')
                            self.mrf.print_world_vars(world)
                            print('GROUND FORMULA:')
                            print('===============')
                            formula.print_structure(world)
                            raise Exception('Something went wrong: Truth of ground formula cannot be evaluated (see above)')
                        if truth in Interval(']0,1['):
                            if formula.weight == HARD:
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

    def forbid_gndatom(self, atom, truth=True):
        """
        Adds a unary constraint that prohibits the given ground atom
        being true.
        """
        atomidx = atom if type(atom) is int else self.mrf.gndatom(atom).idx if type(atom) is str else atom.idx
        varidx = self.atom2var[atomidx]
        variable = self.variables[varidx]
        evidence = list(self.mrf.evidence)
        evidence[atomidx] = {True:1,  False:0}[truth]
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
        if isinstance(gndAtom, str):
            gndAtom = self.mrf.gndAtoms[gndAtom]
        elif not isinstance(gndAtom, Logic.GroundAtom):
            raise Exception('Argument must be a ground atom')
        else:
            varIdx = self.gndAtom2VarIndex[gndAtom]
            valIndices = list(range(len(self.varIdx2GndAtom[varIdx])))
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
                        raise
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

        return dict([(a, c) for a, c in zip(atoms, cost)])


if __name__ == '__main__':
    pass