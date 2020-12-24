# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python3/pracmln/mln/grounding/default.py
# Compiled at: 2018-04-24 04:48:32
# Size of source mod 2**32: 7676 bytes
from dnutils import logs, ProgressBar, ifnone
from ..util import fstr, dict_union, StopWatch
from ..constants import auto, HARD
from ..errors import SatisfiabilityException
logger = logs.getlogger(__name__)
CACHE_SIZE = 100000

class DefaultGroundingFactory:
    __doc__ = '\n    Implementation of the default grounding algorithm, which\n    creates ALL ground atoms and ALL ground formulas.\n\n    :param simplify:        if `True`, the formula will be simplified according to the\n                            evidence given.\n    :param unsatfailure:    raises a :class:`mln.errors.SatisfiabilityException` if a \n                            hard logical constraint is violated by the evidence.\n    '

    def __init__(self, mrf, simplify=False, unsatfailure=False, formulas=None, cache=auto, **params):
        self.mrf = mrf
        self.formulas = ifnone(formulas, list(self.mrf.formulas))
        self.total_gf = 0
        for f in self.formulas:
            self.total_gf += f.countgroundings(self.mrf)

        self.grounder = None
        self._cachesize = CACHE_SIZE if cache is auto else cache
        self._cache = None
        self._DefaultGroundingFactory__cacheinit = False
        self._DefaultGroundingFactory__cachecomplete = False
        self._params = params
        self.watch = StopWatch()
        self.simplify = simplify
        self.unsatfailure = unsatfailure

    @property
    def verbose(self):
        return self._params.get('verbose', False)

    @property
    def multicore(self):
        return self._params.get('multicore', False)

    @property
    def iscached(self):
        return self._cache is not None and self._DefaultGroundingFactory__cacheinit

    @property
    def usecache(self):
        return self._cachesize is not None and self._cachesize > 0

    def _cacheinit(self):
        self._cache = []
        self._DefaultGroundingFactory__cacheinit = True

    def itergroundings(self):
        """
        Iterates over all formula groundings.
        """
        self.watch.tag('grounding', verbose=self.verbose)
        if self.grounder is None:
            self.grounder = iter(self._itergroundings(simplify=self.simplify, unsatfailure=self.unsatfailure))
        if self.usecache and not self.iscached:
            self._cacheinit()
        counter = -1
        while True:
            counter += 1
            if self.iscached and len(self._cache) > counter:
                yield self._cache[counter]
            else:
                if not self._DefaultGroundingFactory__cachecomplete:
                    try:
                        gf = next(self.grounder)
                    except StopIteration:
                        self._DefaultGroundingFactory__cachecomplete = True
                        return
                    else:
                        if self._cache is not None:
                            self._cache.append(gf)
                        yield gf
                else:
                    return

        self.watch.finish('grounding')
        if self.verbose:
            print()

    def _itergroundings(self, simplify=False, unsatfailure=False):
        if self.verbose:
            bar = ProgressBar(color='green')
        for i, formula in enumerate(self.formulas):
            if self.verbose:
                bar.update((i + 1) / float(len(self.formulas)))
            for gndformula in formula.itergroundings(self.mrf, simplify=simplify):
                if unsatfailure and gndformula.weight == HARD and gndformula(self.mrf.evidence) == 0:
                    print()
                    gndformula.print_structure(self.mrf.evidence)
                    raise SatisfiabilityException('MLN is unsatisfiable due to hard constraint violation %s (see above)' % self.mrf.formulas[gndformula.idx])
                yield gndformula


class EqualityConstraintGrounder(object):
    __doc__ = '\n    Grounding factory for equality constraints only.\n    '

    def __init__(self, mrf, domains, mode, eq_constraints):
        """
        Initialize the equality constraint grounder with the given MLN
        and formula. A formula is required that contains all variables
        in the equalities in order to infer the respective domain names.
        
        :param mode: either ``alltrue`` or ``allfalse``
        """
        self.constraints = eq_constraints
        self.mrf = mrf
        self.truth = {'alltrue': 1, 'allfalse': 0}[mode]
        self.mode = mode
        eqvars = [c for eq in eq_constraints if self.mrf.mln.logic.isvar(c) for c in eq]
        self.vardomains = dict([(v, d) for v, d in domains.items() if v in eqvars])

    def iter_valid_variable_assignments(self):
        """
        Yields all variable assignments for which all equality constraints
        evaluate to true.
        """
        return self._iter_valid_variable_assignments(list(self.vardomains.keys()), {}, self.constraints)

    def _iter_valid_variable_assignments(self, variables, assignments, eq_groundings):
        if not variables:
            yield assignments
            return
        eq_groundings = [eq for eq in eq_groundings if not all([not self.mrf.mln.logic.isvar(a) for a in eq.args])]
        variable = variables[0]
        for value in self.mrf.domains[self.vardomains[variable]]:
            new_eq_groundings = []
            goon = True
            for eq in eq_groundings:
                geq = eq.ground(None, {variable: value}, partial=True)
                t = geq(None)
                if t is not None and t != self.truth:
                    goon = False
                    break
                new_eq_groundings.append(geq)

            if not goon:
                pass
            else:
                for assignment in self._iter_valid_variable_assignments(variables[1:], dict_union(assignments, {variable: value}), new_eq_groundings):
                    yield assignment

    @staticmethod
    def vardoms_from_formula(mln, formula, *varnames):
        if isinstance(formula, str):
            formula = mln.logic.parse_formula(formula)
        vardomains = {}
        f_vardomains = formula.vardoms(mln)
        for var in varnames:
            if var not in f_vardomains:
                raise Exception('Variable %s not bound to a domain by formula %s' % (var, fstr(formula)))
            vardomains[var] = f_vardomains[var]

        return vardomains