# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nyga/work/code/pracmln/python2/pracmln/mln/learning/sll.py
# Compiled at: 2018-04-24 04:48:32
import sys
from common import *
from ll import *
from pracmln import logic

class MCMCSampler(object):

    def __init__(self, mrf, mcsatParams, discardDuplicateWorlds=False, keepTopWorldCounts=False, computeHessian=False):
        self.mrf = mrf
        self.N = len(self.mrf.mln.formulas)
        self.wtsLast = None
        self.mcsatParams = mcsatParams
        self.keepTopWorldCounts = keepTopWorldCounts
        if keepTopWorldCounts:
            self.topWorldValue = 0.0
        self.computeHessian = computeHessian
        self.discardDuplicateWorlds = discardDuplicateWorlds
        return

    def sample(self, wtFull):
        if self.wtsLast is None or numpy.any(self.wtsLast != wtFull):
            self.wtsLast = wtFull.copy()
            N = self.N
            self.sampledWorlds = {}
            self.numSamples = 0
            self.Z = 0
            self.globalFormulaCounts = numpy.zeros(N, numpy.float64)
            self.scaledGlobalFormulaCounts = numpy.zeros(N, numpy.float64)
            self.currentWeights = wtFull
            if self.computeHessian:
                self.hessian = None
                self.hessianProd = numpy.zeros((N, N), numpy.float64)
            self.mrf.mln.setWeights(wtFull)
            print 'calling MCSAT with weights:', wtFull
            what = [
             logic.FirstOrderLogic.TrueFalse(True)]
            mcsat = self.mrf.inferMCSAT(what, sampleCallback=self._sampleCallback, **self.mcsatParams)
            print 'sampled %d worlds' % self.numSamples
        else:
            print 'using cached values, no sampling (weights did not change)'
        return

    def _sampleCallback(self, sample, step):
        world = sample.chains[0].state
        if self.discardDuplicateWorlds:
            t = tuple(world)
            if t in self.sampledWorlds:
                return
            self.sampledWorlds[t] = True
        formulaCounts = self.mrf.countTrueGroundingsInWorld(world)
        exp_sum = exp(numpy.sum(formulaCounts * self.currentWeights))
        self.globalFormulaCounts += formulaCounts
        self.scaledGlobalFormulaCounts += formulaCounts * exp_sum
        self.Z += exp_sum
        self.numSamples += 1
        if self.keepTopWorldCounts and exp_sum > self.topWorldValue:
            self.topWorldFormulaCounts = formulaCounts
        if self.computeHessian:
            for i in xrange(self.N):
                self.hessianProd[i][i] += formulaCounts[i] ** 2
                for j in xrange(i + 1, self.N):
                    v = formulaCounts[i] * formulaCounts[j]
                    self.hessianProd[i][j] += v
                    self.hessianProd[j][i] += v

        if self.numSamples % 1000 == 0:
            print '  MCSAT sample #%d' % self.numSamples

    def getHessian(self):
        if not self.computeHessian:
            raise Exception('The Hessian matrix was not computed for this learning method')
        if self.hessian is not None:
            return self.hessian
        else:
            self.hessian = numpy.zeros((self.N, self.N), numpy.float64)
            eCounts = self.globalFormulaCounts / self.numSamples
            for i in xrange(self.N):
                for j in xrange(self.N):
                    self.hessian[i][j] = eCounts[i] * eCounts[j]

            self.hessian -= self.hessianProd / self.numSamples
            return self.hessian

    def getCovariance(self):
        return -self.getHessian()


class SLL(AbstractLearner):
    """
        sample-based log-likelihood
    """

    def __init__(self, mrf, **params):
        AbstractLearner.__init__(self, mrf, **params)
        if len(filter(lambda b: isinstance(b, SoftMutexBlock), self.mrf.gndAtomicBlocks)) > 0:
            raise Exception('%s cannot handle soft-functional constraints' % self.__class__.__name__)
        self.mcsatSteps = self.params.get('mcsatSteps', 2000)
        self.samplerParams = dict(given='', softEvidence={}, maxSteps=self.mcsatSteps, doProbabilityFitting=False, verbose=False, details=False, infoInterval=100, resultsInterval=100)
        self.samplerConstructionParams = dict(discardDuplicateWorlds=False, keepTopWorldCounts=False)

    def _sample(self, wt, caller):
        self.normSampler.sample(wt)

    def _f(self, wt, **params):
        self._sample(wt, 'f')
        ll = numpy.sum(self.formulaCountsTrainingDB * wt) - numpy.sum(self.normSampler.globalFormulaCounts * wt) / self.normSampler.numSamples
        return ll

    def _grad(self, wt, **params):
        self._sample(wt, 'grad')
        grad = self.formulaCountsTrainingDB - self.normSampler.globalFormulaCounts / self.normSampler.numSamples
        return grad

    def _initSampler(self):
        self.normSampler = MCMCSampler(self.mrf, self.samplerParams, **self.samplerConstructionParams)

    def _prepareOpt(self):
        print 'computing counts for training database...'
        self.formulaCountsTrainingDB = self.mrf.countTrueGroundingsInWorld(self.mrf.evidence)
        self._initSampler()


class SLL_DN(SLL):
    """
        sample-based log-likelihood via diagonal Newton
    """

    def __init__(self, mrf, **params):
        SLL.__init__(self, mrf, **params)
        self.samplerConstructionParams['computeHessian'] = True

    def _f(self, wt, **params):
        raise Exception('Objective function not implemented; use e.g. diagonal Newton to optimize')

    def _hessian(self, wt):
        self._sample(wt, 'hessian')
        return self.normSampler.getHessian()

    def getAssociatedOptimizerName(self):
        return 'diagonalNewton'


from softeval import truthDegreeGivenSoftEvidence