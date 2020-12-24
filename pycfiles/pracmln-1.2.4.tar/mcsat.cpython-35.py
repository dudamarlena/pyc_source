# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python3/pracmln/mln/inference/mcsat.py
# Compiled at: 2018-04-24 04:48:32
# Size of source mod 2**32: 30945 bytes
import math, random
from collections import defaultdict
from dnutils import logs, ProgressBar, out
from .mcmc import MCMCInference
from ..constants import ALL, HARD
from ..grounding.fastconj import FastConjunctionGrounding
from ..util import item
from ...logic.common import Logic
logger = logs.getlogger(__name__)

class MCSAT(MCMCInference):
    __doc__ = ' \n    MC-SAT/MC-SAT-PC\n    '

    def __init__(self, mrf, queries=ALL, **params):
        MCMCInference.__init__(self, mrf, queries, **params)
        self._weight_backup = list(self.mrf.mln.weights)

    def _initkb(self, verbose=False):
        """
        Initialize the knowledge base to the required format and collect structural information for optimization purposes
        """
        logger.debug('converting formulas to cnf...')
        self.formulas = []
        for f in self.mrf.formulas:
            if f.weight < 0:
                f.weight = -f.weight
                f = self.mln.logic.negate(f)
            self.formulas.append(f)

        grounder = FastConjunctionGrounding(self.mrf, formulas=self.formulas, simplify=True, verbose=self.verbose)
        self.gndformulas = []
        for gf in grounder.itergroundings():
            if isinstance(gf, Logic.TrueFalse):
                pass
            else:
                self.gndformulas.append(gf.cnf())

        self._watch.tags.update(grounder.watch.tags)
        logger.debug('gathering clause data...')
        self.gf2clauseidx = {}
        self.clauses = []
        i_clause = 0
        for i_gf, gf in enumerate(self.gndformulas):
            if isinstance(gf, Logic.Conjunction):
                clauses = [clause for clause in gf.children if not isinstance(clause, Logic.TrueFalse)]
            elif not isinstance(gf, Logic.TrueFalse):
                clauses = [
                 gf]
            else:
                continue
            self.gf2clauseidx[i_gf] = (
             i_clause, i_clause + len(clauses))
            for c in clauses:
                if hasattr(c, 'children'):
                    lits = c.children
                else:
                    lits = [
                     c]
                self.clauses.append(lits)
                i_clause += 1

        for se in []:
            se['numTrue'] = 0.0
            formula = self.mln.logic.parseFormula(se['expr'])
            se['formula'] = formula.ground(self.mrf, {})
            cnf = formula.toCNF().ground(self.mrf, {})
            idxFirst = i_clause
            for clause in self._formulaClauses(cnf):
                self.clauses.append(clause)
                i_clause += 1

            se['idxClausePositive'] = (
             idxFirst, i_clause)
            cnf = self.mln.logic.negation([formula]).toCNF().ground(self.mrf, {})
            idxFirst = i_clause
            for clause in self._formulaClauses(cnf):
                self.clauses.append(clause)
                i_clause += 1

            se['idxClauseNegative'] = (
             idxFirst, i_clause)

    def _formula_clauses(self, f):
        if isinstance(f, Logic.Conjunction):
            lc = f.children
        else:
            lc = [
             f]
        for c in lc:
            if hasattr(c, 'children'):
                yield c.children
            else:
                yield [
                 c]

    @property
    def chains(self):
        return self._params.get('chains', 1)

    @property
    def maxsteps(self):
        return self._params.get('maxsteps', 500)

    @property
    def softevidence(self):
        return self._params.get('softevidence', False)

    @property
    def use_se(self):
        return self._params.get('use_se')

    @property
    def p(self):
        return self._params.get('p', 0.5)

    @property
    def resulthistory(self):
        return self._params.get('resulthistory', False)

    @property
    def historyfile(self):
        return self._params.get('historyfile', None)

    @property
    def rndseed(self):
        return self._params.get('rndseed', None)

    @property
    def initalgo(self):
        return self._params.get('initalgo', 'SampleSAT')

    def _run(self):
        """
        p: probability of a greedy (WalkSAT) move
        initAlgo: algorithm to use in order to find an initial state that satisfies all hard constraints ("SampleSAT" or "SAMaxWalkSat")
        verbose: whether to display results upon completion
        details: whether to display information while the algorithm is running            
        infoInterval: [if details==True] interval (no. of steps) in which to display the current step number and some additional info
        resultsInterval: [if details==True] interval (no. of steps) in which to display intermediate results; [if keepResultsHistory==True] interval in which to store intermediate results in the history
        debug: whether to display debug information (e.g. internal data structures) while the algorithm is running
            debugLevel: controls degree to which debug information is presented
        keepResultsHistory: whether to store the history of results (at each resultsInterval)
        referenceResults: reference results to compare obtained results to
        saveHistoryFile: if not None, save history to given filename
        sampleCallback: function that is called for every sample with the sample and step number as parameters
        softEvidence: if None, use soft evidence from MLN, otherwise use given dictionary of soft evidence
        handleSoftEvidence: if False, ignore all soft evidence in the MCMC sampling (but still compute softe evidence statistics if soft evidence is there)
        """
        logger.debug('starting MC-SAT with maxsteps=%d, softevidence=%s' % (self.maxsteps, self.softevidence))
        self._initkb()
        logger.debug('CNF KB:')
        for gf in self.gndformulas:
            logger.debug('%7.3f  %s' % (gf.weight, str(gf)))

        print()
        if self.rndseed is not None:
            random.seed(self.rndseed)
        chaingroup = MCMCInference.ChainGroup(self)
        self.chaingroup = chaingroup
        for i in range(self.chains):
            chain = MCMCInference.Chain(self, self.queries)
            chaingroup.chain(chain)
            M = []
            NLC = []
            for i, gf in enumerate(self.gndformulas):
                if gf.weight == HARD:
                    if gf.islogical():
                        clause_range = self.gf2clauseidx[i]
                        M.extend(list(range(*clause_range)))
                    else:
                        NLC.append(gf)

            if M or NLC:
                logger.debug('Running SampleSAT')
                chain.state = SampleSAT(self.mrf, chain.state, M, NLC, self, p=self.p).run()

        if logger.level == logs.DEBUG:
            self.mrf.print_world_vars(chain.state)
        self.step = 1
        logger.debug('running MC-SAT with %d chains' % len(chaingroup.chains))
        self._watch.tag('running MC-SAT', self.verbose)
        if self.verbose:
            bar = ProgressBar(steps=self.maxsteps, color='green')
        while self.step <= self.maxsteps:
            for chain in chaingroup.chains:
                state = self._satisfy_subset(chain)
                chain.update(state)

            if self.verbose:
                bar.inc()
                bar.label('%d / %d' % (self.step, self.maxsteps))
            self.step += 1

        self.step -= 1
        results = chaingroup.results()
        return results[0]

    def _satisfy_subset(self, chain):
        """
        Choose a set of logical formulas M to be satisfied (more specifically, M is a set of clause indices)
        and also choose a set of non-logical constraints NLC to satisfy
        """
        M = []
        NLC = []
        for gfidx, gf in enumerate(self.gndformulas):
            if gf(chain.state) == 1 or gf.ishard:
                expweight = math.exp(gf.weight)
                u = random.uniform(0, expweight)
                if u > 1:
                    if gf.islogical():
                        clause_range = self.gf2clauseidx[gfidx]
                        M.extend(list(range(*clause_range)))
                    else:
                        NLC.append(gf)

        return SampleSAT(self.mrf, chain.state, M, NLC, self, p=self.p).run()

    def _prob_constraints_deviation(self):
        if len(self.softevidence) == 0:
            return {}
        se_mean, se_max, se_max_item = (0.0, -1, None)
        for se in self.softevidence:
            dev = abs(se['numTrue'] / self.step - se['p'])
            se_mean += dev
            if dev > se_max:
                se_max = max(se_max, dev)
                se_max_item = se

        se_mean /= len(self.softevidence)
        return {'pc_dev_mean': se_mean, 'pc_dev_max': se_max, 'pc_dev_max_item': se_max_item['expr']}

    def _extend_results_history(self, results):
        cur_results = {'step': self.step, 'results': list(results), 'time': self._getElapsedTime()[0]}
        cur_results.update(self._getProbConstraintsDeviation())
        if self.referenceResults is not None:
            cur_results.update(self._compareResults(results, self.referenceResults))
        self.history.append(cur_results)

    def getResultsHistory(self):
        return self.resultsHistory


class SampleSAT:
    __doc__ = '\n    Sample-SAT algorithm.\n    '

    def __init__(self, mrf, state, clause_indices, nlcs, infer, p=1):
        """
        clause_indices: list of indices of clauses to satisfy
        p: probability of performing a greedy WalkSAT move
        state: the state (array of booleans) to work with (is reinitialized randomly by this constructor)
        NLConstraints: list of grounded non-logical constraints
        """
        self.debug = logger.level == logs.DEBUG
        self.infer = infer
        self.mrf = mrf
        self.mln = mrf.mln
        self.p = p
        self.blockInfo = {}
        self.state = self.infer.random_world()
        self.init = list(state)
        self.unsatisfied = set()
        self.bottlenecks = defaultdict(list)
        self.var2clauses = defaultdict(set)
        self.clauses = {}
        for cidx in clause_indices:
            clause = SampleSAT._Clause(self.infer.clauses[cidx], self.state, cidx, self.mrf)
            self.clauses[cidx] = clause
            if clause.unsatisfied:
                self.unsatisfied.add(cidx)
            for v in clause.variables():
                self.var2clauses[v].add(clause)

        for nlc in nlcs:
            if isinstance(nlc, Logic.GroundCountConstraint):
                SampleSAT._CountConstraint(self, nlc)
            else:
                raise Exception("SampleSAT cannot handle constraints of type '%s'" % str(type(nlc)))

    def _print_unsatisfied_constraints(self):
        out('   %d unsatisfied:  %s' % (len(self.unsatisfied), list(map(str, [self.clauses[i] for i in self.unsatisfied]))), tb=2)

    def run(self):
        worlds = []
        for world in self.mrf.worlds():
            skip = False
            for clause in list(self.clauses.values()):
                if not clause.satisfied_in_world(world):
                    skip = True
                    break

            if skip:
                pass
            else:
                worlds.append(world)

        state = worlds[random.randint(0, len(worlds) - 1)]
        return state
        steps = 0
        while self.unsatisfied:
            steps += 1
            if random.uniform(0, 1) <= self.p:
                self._walksat_move()
            else:
                self._sa_move()

        return self.state

    def _walksat_move(self):
        """
        Randomly pick one of the unsatisfied constraints and satisfy it
        (or at least make one step towards satisfying it
        """
        clauseidx = list(self.unsatisfied)[random.randint(0, len(self.unsatisfied) - 1)]
        clause = self.clauses[clauseidx]
        varval_opt = []
        opt = None
        for var in clause.variables():
            bottleneck_clauses = [cl for cl in self.var2clauses[var] if cl.bottleneck is not None]
            for _, value in var.itervalues(self.mrf.evidence_dicti()):
                if not clause.turns_true_with(var, value):
                    pass
                else:
                    unsat = 0
                    for c in bottleneck_clauses:
                        turnsfalse = 1 if c.turns_false_with(var, value) else 0
                        unsat += turnsfalse

                    append = False
                    if opt is None or unsat < opt:
                        opt = unsat
                        varval_opt = []
                        append = True
                    elif opt == unsat:
                        append = True
                if append:
                    varval_opt.append((var, value))

        if varval_opt:
            varval = varval_opt[random.randint(0, len(varval_opt) - 1)]
            self._setvar(*varval)

    def _setvar(self, var, val):
        """
        Set the truth value of a variable and update the information in the constraints.
        """
        var.setval(val, self.state)
        for c in self.var2clauses[var]:
            satisfied, _ = c.update(var, val)
            if satisfied:
                if c.cidx in self.unsatisfied:
                    self.unsatisfied.remove(c.cidx)
                else:
                    self.unsatisfied.add(c.cidx)

    def _sa_move(self):
        variables = list(set(self.var2clauses))
        random.shuffle(variables)
        var = variables[0]
        ev = var.evidence_value()
        values = var.valuecount(self.mrf.evidence)
        for _, v in var.itervalues(self.mrf.evidence):
            break

        if values == 1:
            raise Exception('Only one remaining value for variable %s: %s. Please check your evidences.' % (var, v))
        values = [v for _, v in var.itervalues(self.mrf.evidence) if v != ev]
        val = values[random.randint(0, len(values) - 1)]
        unsat = 0
        bottleneck_clauses = [c for c in self.var2clauses[var] if c.bottleneck is not None]
        for c in bottleneck_clauses:
            uns = 1 if c.turns_false_with(var, val) else 0
            unsat += uns

        if unsat <= 0:
            p = 1.0
        else:
            p = math.exp(-1 + float(len(bottleneck_clauses) - unsat) / len(bottleneck_clauses))
        if random.uniform(0, 1) <= p:
            self._setvar(var, val)

    class _Clause(object):

        def __init__(self, lits, world, idx, mrf):
            self.cidx = idx
            self.world = world
            self.bottleneck = None
            self.mrf = mrf
            self.lits = lits
            self.truelits = set()
            self.atomidx2lits = defaultdict(set)
            for lit in lits:
                if isinstance(lit, Logic.TrueFalse):
                    pass
                else:
                    atomidx = lit.gndatom.idx
                    self.atomidx2lits[atomidx].add(0 if lit.negated else 1)
                    if lit(world) == 1:
                        self.truelits.add(atomidx)

            if len(self.truelits) == 1 and self._isbottleneck(item(self.truelits)):
                self.bottleneck = item(self.truelits)

        def _isbottleneck(self, atomidx):
            atomidx2lits = self.atomidx2lits
            if len(self.truelits) != 1 or atomidx not in self.truelits:
                return False
            if len(atomidx2lits[atomidx]) == 1:
                return True
            fst = item(atomidx2lits[atomidx])
            if all([x == fst for x in atomidx2lits[atomidx]]):
                return False
            return True

        def turns_false_with(self, var, val):
            """
            Returns whether or not this clause would become false if the given variable would take
            the given value. Returns False if the clause is already False.
            """
            for a, v in var.atomvalues(val):
                if a.idx == self.bottleneck and v not in self.atomidx2lits[a.idx]:
                    return True

            return False

        def turns_true_with(self, var, val):
            """
            Returns true if this clause will be rendered true by the given variable taking
            its given value.
            """
            for a, v in var.atomvalues(val):
                if self.unsatisfied and v in self.atomidx2lits[a.idx]:
                    return True

            return False

        def update(self, var, val):
            """
            Updates the clause information with the given variable and value set in a SampleSAT state.
            """
            for a, v in var.atomvalues(val):
                if v not in self.atomidx2lits[a.idx]:
                    if a.idx in self.truelits:
                        self.truelits.remove(a.idx)
                    else:
                        self.truelits.add(a.idx)

            if len(self.truelits) == 1 and self._isbottleneck(item(self.truelits)):
                self.bottleneck = item(self.truelits)
            else:
                self.bottleneck = None
            return (
             self.satisfied, self.bottleneck)

        def satisfied_in_world(self, world):
            return self.mrf.mln.logic.disjugate(self.lits)(world) == 1

        @property
        def unsatisfied(self):
            return not self.truelits

        @property
        def satisfied(self):
            return not self.unsatisfied

        def variables(self):
            return [self.mrf.variable(self.mrf.gndatom(a)) for a in self.atomidx2lits]

        def greedySatisfy(self):
            self.ss._pickAndFlipLiteral([x.gndAtom.idx for x in self.lits], self)

        def __str__(self):
            return ' v '.join(map(str, self.lits))

    class _CountConstraint:

        def __init__(self, sampleSAT, groundCountConstraint):
            self.ss = sampleSAT
            self.cc = groundCountConstraint
            self.trueOnes = []
            self.falseOnes = []
            for ga in groundCountConstraint.gndAtoms:
                idxGA = ga.idx
                if self.ss.state[idxGA]:
                    self.trueOnes.append(idxGA)
                else:
                    self.falseOnes.append(idxGA)
                self.ss._addGAOccurrence(idxGA, self)

            self._addBottlenecks()
            if not self._isSatisfied():
                self.ss.unsatisfiedConstraints.append(self)

        def _isSatisfied(self):
            return eval('len(self.trueOnes) %s self.cc.count' % self.cc.op)

        def _addBottlenecks(self):
            numTrue = len(self.trueOnes)
            if self.cc.op == '!=':
                trueNecks = numTrue == self.cc.count + 1
                falseNecks = numTrue == self.cc.count - 1
            else:
                border = numTrue == self.cc.count
                trueNecks = border and self.cc.op in ('==', '>=')
                falseNecks = border and self.cc.op in ('==', '<=')
            if trueNecks:
                for idxGA in self.trueOnes:
                    self.ss._addBottleneck(idxGA, self)

            if falseNecks:
                for idxGA in self.falseOnes:
                    self.ss._addBottleneck(idxGA, self)

        def greedySatisfy(self):
            c = len(self.trueOnes)
            satisfied = self._isSatisfied()
            assert not satisfied
            if c < self.cc.count and not satisfied:
                self.ss._pickAndFlipLiteral(self.falseOnes, self)
            else:
                if c > self.cc.count and not satisfied:
                    self.ss._pickAndFlipLiteral(self.trueOnes, self)
                else:
                    self.ss._pickAndFlipLiteral(self.trueOnes + self.falseOnes, self)

        def flipSatisfies(self, idxGA):
            if self._isSatisfied():
                return False
            c = len(self.trueOnes)
            if idxGA in self.trueOnes:
                c2 = c - 1
            else:
                assert idxGA in self.falseOnes
                c2 = c + 1
            return eval('c2 %s self.cc.count' % self.cc.op)

        def handleFlip(self, idxGA):
            """
            Handle all effects of the flip except bottlenecks of the flipped
            gnd atom and clauses that became unsatisfied as a result of a bottleneck flip
            """
            wasSatisfied = self._isSatisfied()
            if idxGA in self.trueOnes:
                self.trueOnes.remove(idxGA)
                self.falseOnes.append(idxGA)
            else:
                self.trueOnes.append(idxGA)
                self.falseOnes.remove(idxGA)
            isSatisfied = self._isSatisfied()
            if wasSatisfied:
                for idxGndAtom in self.trueOnes + self.falseOnes:
                    if idxGndAtom in self.ss.bottlenecks and self in self.ss.bottlenecks[idxGndAtom] and idxGA != idxGndAtom:
                        self.ss.bottlenecks[idxGndAtom].remove(self)

            elif not wasSatisfied and isSatisfied:
                self.ss.unsatisfiedConstraints.remove(self)
            self._addBottlenecks()

        def __str__(self):
            return str(self.cc)

        def getFormula(self):
            return self.cc