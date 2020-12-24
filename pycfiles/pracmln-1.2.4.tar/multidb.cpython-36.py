# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/code/pracmln/python3/pracmln/mln/learning/multidb.py
# Compiled at: 2019-02-27 05:10:32
# Size of source mod 2**32: 9516 bytes
from dnutils import logs, ProgressBar, out, first
from .common import AbstractLearner
import sys
from ..util import StopWatch, edict
from multiprocessing import Pool
from ...utils.multicore import with_tracing, _methodcaller, checkmem
import numpy
from ..constants import HARD
logger = logs.getlogger(__name__)

def _setup_learner(xxx_todo_changeme):
    i, mln_, db, method, params = xxx_todo_changeme
    checkmem()
    mrf = mln_.ground(db)
    algo = method(mrf, **params)
    return (i, algo)


class MultipleDatabaseLearner(AbstractLearner):
    __doc__ = '\n    Learns from multiple databases using an arbitrary sub-learning method for\n    each database, assuming independence between individual databases.\n    '

    def __init__(self, mln_, dbs, method, **params):
        """
        :param dbs:         list of :class:`mln.database.Database` objects to
                            be used for learning.
        :param mln_:        the MLN object to be used for learning
        :param method:      the algorithm to be used for learning. Must be a
                            class provided by
                            :class:`mln.methods.LearningMethods`.
        :param **params:    additional parameters handed over to the base
                            learners.
        """
        self.dbs = dbs
        self._params = edict(params)
        if not mln_._materialized:
            self.mln = (mln_.materialize)(*dbs)
        else:
            self.mln = mln_
        self.watch = StopWatch()
        self.learners = [None] * len(dbs)
        self.watch.tag('setup learners', verbose=(self.verbose))
        if self.verbose:
            bar = ProgressBar(steps=(len(dbs)), color='green')
        else:
            if self.multicore:
                pool = Pool(maxtasksperchild=1)
                logger.debug('Setting up multi-core processing for {} cores'.format(pool._processes))
                try:
                    try:
                        for i, learner in pool.imap(with_tracing(_setup_learner), self._iterdbs(method)):
                            self.learners[i] = learner
                            if self.verbose:
                                bar.label('Database %d, %s' % (i + 1, learner.name))
                                bar.inc()

                    except Exception as e:
                        logger.error('Error in child process. Terminating pool...')
                        pool.close()
                        raise e

                finally:
                    pool.terminate()
                    pool.join()

                self.mln.weights = list(first(self.learners).mrf.mln.weights)
            else:
                for i, db in enumerate(self.dbs):
                    _, learner = _setup_learner((i, self.mln, db, method, self._params + {'multicore': False}))
                    self.learners[i] = learner
                    if self.verbose:
                        bar.label('Database %d, %s' % (i + 1, learner.name))
                        bar.inc()

        if self.verbose:
            print('set up', self.name)
        self.watch.finish('setup learners')

    def _iterdbs(self, method):
        for i, db in enumerate(self.dbs):
            yield (i, self.mln, db, method,
             self._params + {'verbose':not self.multicore, 
              'multicore':False})

    @property
    def name(self):
        return 'MultipleDatabaseLearner [{} x {}]'.format(len(self.learners), self.learners[0].name)

    def _f(self, w):
        return sum([l._f(w) for l in self.learners])

    def _grad(self, w):
        grad = numpy.zeros(len(self.mln.formulas), numpy.float64)
        for learner in self.learners:
            grad += learner._grad(w)

        return grad

    def _hessian(self, w):
        N = len(self.mln.formulas)
        hessian = numpy.matrix(numpy.zeros((N, N)))
        if self.multicore:
            pool = Pool()
            try:
                try:
                    for h in pool.imap(with_tracing(_methodcaller('_hessian')), [(l, w) for l in self.learners]):
                        hessian += h

                except Exception as e:
                    logger.error('Error in child process. Terminating pool...')
                    pool.close()
                    raise e

            finally:
                pool.terminate()
                pool.join()

        else:
            for learner in self.learners:
                hessian += learner._hessian(w)

        return hessian

    def _prepare(self):
        self.watch.tag('preparing optimization', verbose=(self.verbose))
        if self.verbose:
            bar = ProgressBar(steps=(len(self.dbs)), color='green')
        else:
            if self.multicore:
                pool = Pool(maxtasksperchild=1)
                try:
                    try:
                        for i, (_, d_) in enumerate(pool.imap(with_tracing(_methodcaller('_prepare', sideeffects=True)), self.learners)):
                            checkmem()
                            self.learners[i].__dict__ = d_
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
                for learner in self.learners:
                    checkmem()
                    learner._prepare()
                    if self.verbose:
                        bar.inc()

    def _filter_fixweights(self, v):
        """
        Removes from the vector `v` all elements at indices that correspond to
        a fixed weight formula index.
        """
        if len(v) != len(self.mln.formulas):
            raise Exception('Vector must have same length as formula weights')
        return [v[i] for i in range(len(self.mln.formulas)) if not self.mln.fixweights[i] if self.mln.weights[i] != HARD]

    def _add_fixweights(self, w):
        i = 0
        w_ = []
        for f in self.mln.formulas:
            if self.mln.fixweights[f.idx] or f.weight == HARD:
                w_.append(self._w[f.idx])
            else:
                w_.append(w[i])
                i += 1

        return w_

    def run(self, **params):
        if 'scipy' not in sys.modules:
            raise Exception('Scipy was not imported! Install numpy and scipy if you want to use weight learning.')
        runs = 0
        self._w = [0] * len(self.mln.formulas)
        while runs < self.maxrepeat:
            self._prepare()
            for f in self.mln.formulas:
                if self.mln.fixweights[f.idx] or self.use_init_weights or f.ishard:
                    self._w[f.idx] = f.weight

            (self._optimize)(**self._params)
            self._cleanup()
            runs += 1
            if not any([l.repeat() for l in self.learners]):
                break

        return self.weights