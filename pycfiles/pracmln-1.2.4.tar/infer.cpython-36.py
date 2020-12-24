# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/code/pracmln/python3/pracmln/mln/inference/infer.py
# Compiled at: 2019-02-27 05:10:32
# Size of source mod 2**32: 10745 bytes
from dnutils import logs
from dnutils.console import barstr
from ...logic.common import Logic
from ..database import Database
from ..constants import ALL
from ..mrfvars import MutexVariable, SoftMutexVariable, FuzzyVariable
from ..util import StopWatch, elapsed_time_str, headline, tty, edict
import sys
from ..errors import NoSuchPredicateError
from ..mlnpreds import SoftFunctionalPredicate, FunctionalPredicate
from functools import reduce
logger = logs.getlogger(__name__)

class Inference(object):
    __doc__ = '\n    Represents a super class for all inference methods.\n    Also provides some convenience methods for collecting statistics\n    about the inference process and nicely outputting results.\n    \n    :param mrf:        the MRF inference is being applied to.\n    :param queries:    a query or list of queries, can be either instances of\n                       :class:`pracmln.logic.common.Logic` or string representations of them,\n                       or predicate names that get expanded to all of their ground atoms.\n                       If `ALL`, all ground atoms are subject to inference.\n                       \n    Additional keyword parameters:\n    \n    :param cw:         (bool) if `True`, the closed-world assumption will be applied \n                       to all but the query atoms.\n    '

    def __init__(self, mrf, queries=ALL, **params):
        self.mrf = mrf
        self.mln = mrf.mln
        self._params = edict(params)
        if not queries:
            self.queries = [self.mln.logic.gnd_lit(ga, negated=False, mln=(self.mln)) for ga in self.mrf.gndatoms if self.mrf.evidence[ga.idx] is None]
        else:
            if type(queries) is not list:
                queries = [
                 queries]
            self.queries = self._expand_queries(queries)
        for variable in self.mrf.variables:
            if variable.valuecount(self.mrf.evidence_dicti()) == 1:
                for _, value in variable.itervalues(self.mrf.evidence):
                    break

                self.mrf.set_evidence((variable.value2dict(value)), erase=False)

        if self.cwpreds:
            for pred in self.cwpreds:
                if isinstance(self.mln.predicate(pred), SoftFunctionalPredicate):
                    if self.verbose:
                        logger.warning('Closed world assumption will be applied to soft functional predicate %s' % pred)
                else:
                    if isinstance(self.mln.predicate(pred), FunctionalPredicate):
                        raise Exception('Closed world assumption is inapplicable to functional predicate %s' % pred)
                    for gndatom in self.mrf.gndatoms:
                        if gndatom.predname != pred:
                            pass
                        else:
                            if self.mrf.evidence[gndatom.idx] is None:
                                self.mrf.evidence[gndatom.idx] = 0

        if self.closedworld:
            qpreds = set()
            for q in self.queries:
                qpreds.update(q.prednames())

            for gndatom in self.mrf.gndatoms:
                if not isinstance(self.mln.predicate(gndatom.predname), FunctionalPredicate):
                    if isinstance(self.mln.predicate(gndatom.predname), SoftFunctionalPredicate):
                        pass
                    elif gndatom.predname not in qpreds and self.mrf.evidence[gndatom.idx] is None:
                        self.mrf.evidence[gndatom.idx] = 0

        for var in self.mrf.variables:
            if isinstance(var, FuzzyVariable):
                var.consistent((self.mrf.evidence), strict=True)

        self._watch = StopWatch()

    @property
    def verbose(self):
        return self._params.get('verbose', False)

    @property
    def results(self):
        if self._results is None:
            raise Exception('No results available. Run the inference first.')
        else:
            return self._results

    @property
    def elapsedtime(self):
        return self._watch['inference'].elapsedtime

    @property
    def multicore(self):
        return self._params.get('multicore')

    @property
    def resultdb(self):
        if '_resultdb' in self.__dict__:
            return self._resultdb
        else:
            db = Database(self.mrf.mln)
            for atom in sorted((self.results), key=str):
                db[str(atom)] = self.results[atom]

            return db

    @resultdb.setter
    def resultdb(self, db):
        self._resultdb = db

    @property
    def closedworld(self):
        return self._params.get('cw', False)

    @property
    def cwpreds(self):
        return self._params.get('cw_preds', [])

    def _expand_queries(self, queries):
        """ 
        Expands the list of queries where necessary, e.g. queries that are 
        just predicate names are expanded to the corresponding list of atoms.
        """
        equeries = []
        for query in queries:
            if type(query) == str:
                prevLen = len(equeries)
                if '(' in query:
                    f = self.mln.logic.parse_formula(query)
                    for gf in f.itergroundings(self.mrf):
                        equeries.append(gf)

                else:
                    if query not in self.mln.prednames:
                        raise NoSuchPredicateError('Unsupported query: %s is not among the admissible predicates.' % query)
                        continue
                    for gndatom in self.mln.predicate(query).groundatoms(self.mln, self.mrf.domains):
                        equeries.append(self.mln.logic.gnd_lit((self.mrf.gndatom(gndatom)), negated=False, mln=(self.mln)))

                if len(equeries) - prevLen == 0:
                    raise Exception("String query '%s' could not be expanded." % query)
            else:
                if isinstance(query, Logic.Formula):
                    equeries.append(query)
                else:
                    raise Exception("Received query of unsupported type '%s'" % str(type(query)))

        return equeries

    def _run(self):
        raise Exception('%s does not implement _run()' % self.__class__.__name__)

    def run(self):
        """
        Starts the inference process.
        """
        if self.verbose:
            print('Inference engine: %s' % self.__class__.__name__)
        self._watch.tag('inference', verbose=(self.verbose))
        _weights_backup = list(self.mln.weights)
        self._results = self._run()
        self.mln.weights = _weights_backup
        self._watch.finish('inference')
        return self

    def write(self, stream=sys.stdout, color=None, sort='prob', group=True, reverse=True):
        barwidth = 30
        if tty(stream):
            if color is None:
                color = 'yellow'
        if sort not in ('alpha', 'prob'):
            raise Exception('Unknown sorting: %s' % sort)
        results = dict(self.results)
        if group:
            wrote_results = False
            for var in sorted((self.mrf.variables), key=str):
                res = dict([(atom, prob) for atom, prob in results.items() if atom in list(map(str, var.gndatoms))])
                if not res:
                    pass
                else:
                    if isinstance(var, MutexVariable) or isinstance(var, SoftMutexVariable):
                        stream.write('%s:\n' % var)
                    if sort == 'prob':
                        res = sorted(res, key=(self.results.__getitem__), reverse=reverse)
                    else:
                        if sort == 'alpha':
                            res = sorted(res, key=str)
                    for atom in res:
                        stream.write('%s %s\n' % (barstr(barwidth, (self.results[atom]), color=color), atom))

                wrote_results = True

            if not wrote_results:
                max_len = max([len(str(q)) for q, p in list(results.items())])
                result_tuples = list(results.items())
                result_tuples.sort(key=(lambda pair: pair[1]), reverse=True)
                str_results = [('{:' + str(max_len) + 's}  {:7.2f}').format(str(q), p) for q, p in result_tuples]
                stream.write(reduce(lambda a, b: a + '\n' + b, str_results, ''))
            return
        results = sorted(results, key=(self.results.__getitem__), reverse=reverse)
        results = sorted(results, key=str)
        for q in results:
            stream.write('%s %s\n' % (barstr(barwidth, (self.results[q]), color=color), q))

        self._watch.printSteps()

    def write_elapsed_time(self, stream=sys.stdout, color=None):
        if stream is sys.stdout:
            if color is None:
                color = True
        else:
            if color is None:
                color = False
            if color:
                col = 'blue'
            else:
                col = None
        total = float(self._watch['inference'].elapsedtime)
        stream.write(headline('INFERENCE RUNTIME STATISTICS'))
        print()
        self._watch.finish()
        for t in sorted((list(self._watch.tags.values())), key=(lambda t: t.elapsedtime), reverse=True):
            stream.write('%s %s %s\n' % (barstr(width=30, percent=(t.elapsedtime / total), color=col), elapsed_time_str(t.elapsedtime), t.label))