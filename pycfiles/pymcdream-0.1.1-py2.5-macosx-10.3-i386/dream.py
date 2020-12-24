# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/pymcdream/dream.py
# Compiled at: 2009-12-18 22:02:19
"""
Created on Oct 24, 2009

@author: johnsalvatier
"""
from __future__ import division
from pymc import *
from numpy import *
from scipy.stats import scoreatpercentile
from rand_no_replace import *
import time

class DreamSampler():
    """
    DREAM sampling object. 
    
    Contains multiple DreamChain(MCMC) objects which each use a DreamStepper step method. 
    The DreamSampler coordinates their stepping.
    """
    _model_generator = None
    _chains = []
    _chain_model = []
    _numbers = None
    outliersFound = 0
    acceptRatio = 0.0

    def __init__(self, model_generator):
        """
        Initializes the sampler.
        
        Parameters
        ----------
            model_generator : func()
                a parameterless function which returns a collection of Stochastics which make up the model. 
                Will be called multiple times, once for each chain. If the Stochastics returned are not identical 
                (for example, based on different data) and distinct (separately instanced) the sampler will have problems.  
        """
        self._model_generator = model_generator

    def sample(self, ndraw=5000, ndraw_max=1000000, nChains=10, burnInSize=500, nCR=5, DEpairs=1, eps=0.05):
        """
        Samples from a posterior distribution using DREAM.
        
        Parameters
        ----------
        ndraw : int 
            minimum number of draws from the sample distribution to be returned 
        ndraw_max : int 
            maximum number of draws from the sample distribution to be returned
        nChains : int 
            number of different chains to employ
        burnInSize : int
            number of iterations (meaning draws / nChains) to do before doing actual sampling.
        nCR : int
            number of intervals to use to adjust the crossover probability distribution for efficiency
        DEpairs : int 
            number of pairs of chains to base movements off of
        eps : float
            used in jittering the chains
            
        Returns
        -------
            None : None 
                sample sets 
                self.history which contains the combined draws for all the chains
                self.iter which is the total number of iterations 
                self.acceptRatio which is the acceptance ratio
                self.burnIn which is the number of burn in iterations done 
                self.R  which is the gelman rubin convergence diagnostic for each dimension
        """
        burnIn = burnInSize
        _chains = []
        for i in range(nChains):
            model = self._model_generator()
            chain = DreamChain(self, model)
            chain.sampleInit(ndraw_max)
            _chains.append(chain)

        accepts = 0
        dimensions = _chains[0].currentVector().shape[0]
        gamma = None
        self._numbers = arange(nCR)
        maxChainDraws = floor(ndraw_max / nChains)
        history = zeros((nChains * maxChainDraws, dimensions))
        sequences = zeros((nChains, dimensions, maxChainDraws))
        logPSequences = zeros((nChains, maxChainDraws))
        grConvergence = GRConvergence()
        currentVectors = zeros((nChains, dimensions))
        currentLogPs = zeros(nChains)
        for i in range(nChains):
            currentVectors[i, :] = _chains[i].currentVector()
            currentLogPs[i] = _chains[i].logp()

        Pm = ones(nCR) / nCR
        L = zeros(nCR)
        deltas = zeros(nCR)
        minDrawIters = ceil(ndraw / nChains)
        maxIters = ceil(ndraw_max / nChains)
        iter = 0
        draws = 0
        while (iter < minDrawIters * 2 + burnIn or any(grConvergence.R > 1.1)) and iter < maxIters:
            m = self._getMs(nChains, Pm)
            crProbabilities = (m + 1) / float(nCR)
            if iter < burnIn:
                L[m] += 1
            crDecisions = random.binomial(1, crProbabilities[:, newaxis], size=(nChains, dimensions))
            if iter % 5 == 0.0:
                gamma = array([1.0])
            else:
                gamma = 2.38 / sqrt(2 * DEpairs * sum(crDecisions, axis=1))
            proposalVectors = self._propose(currentVectors, dimensions, nChains, DEpairs, gamma, eps)
            proposalVectors = choose(crDecisions, (currentVectors, proposalVectors))
            proposalLogPs = zeros(nChains)
            for i in range(nChains):
                _chains[i].propose(proposalVectors[i, :], iter)
                try:
                    proposalLogPs[i] = _chains[i].logp()
                except ZeroProbability:
                    proposalLogPs[i] = -Inf

            decisions = self._decide(currentLogPs, proposalLogPs, nChains)
            accepts += sum(decisions)
            for i in range(nChains):
                if decisions[i] == False:
                    _chains[i].reject()

            previousVectors = currentVectors
            currentVectors = choose(decisions[:, newaxis], (currentVectors, proposalVectors))
            currentLogPs = choose(decisions, (currentLogPs, proposalLogPs))
            if iter > burnIn:
                history[draws:draws + nChains, :] = currentVectors
            sequences[:, :, iter] = currentVectors
            logPSequences[:, iter] = currentLogPs
            if iter < burnIn:
                vars = var(currentVectors, axis=0)
                deltas[m] = deltas[m] + sum((currentVectors - previousVectors) ** 2 / vars, axis=1)
                if all(L > 10):
                    if all(deltas > 0):
                        Pm = (iter + 1) * nChains * (deltas / L) / sum(deltas)
                        Pm = Pm / sum(Pm)
                if iter < burnIn and iter > burnInSize / 2:
                    logPMeans = mean(logPSequences[:, iter / 2:iter], axis=1)
                    Q1 = scoreatpercentile(logPMeans, 25)
                    IQR = scoreatpercentile(logPMeans, 75) - Q1
                    isOutlierChain = logPMeans < Q1 - 2 * IQR
                    if any(isOutlierChain):
                        best = argmax(currentLogPs)
                        for i in range(nChains):
                            if isOutlierChain[i]:
                                _chains[i].propose(currentVectors[best, :], iter)

                        burnIn = burnInSize + iter
                        self.outliersFound += 1
                if iter > burnIn + minDrawIters * 2:
                    grConvergence.update(sequences, burnIn, iter, dimensions, nChains)
                iter += 1
            elif iter > burnIn:
                draws += nChains

        self.history = history[draws / 2.0:draws, :]
        self.iter = iter
        self.acceptRatio = accepts * 1.0 / (iter * nChains)
        self.burnIn = burnIn
        self.R = grConvergence.R
        for i in range(nChains):
            _chains[i].sampleFinalize()

        return

    def _propose(self, currentVectors, dimensions, nChains, DEpairs, gamma, eps):
        """
        generates and returns proposal vectors given the current states
        """
        currentIndex = arange(0, nChains)[:, newaxis]
        chains = random_no_replace(DEpairs * 2, nChains - 1, nChains)
        chains += chains >= currentIndex
        chainDifferences = sum(currentVectors[chains[:, 0:DEpairs], :], axis=1) - sum(currentVectors[chains[:, DEpairs:DEpairs * 2], :], axis=1)
        e = numpy.random.uniform(-eps, eps, size=(nChains, dimensions))
        E = numpy.random.normal(0, eps, (nChains, dimensions))
        proposalVectors = currentVectors + (1 + e) * gamma[:, newaxis] * chainDifferences + E
        return proposalVectors

    def _getMs(self, nChains, pCRs):
        return sum(self._numbers[newaxis, :] * random.multinomial(1, pCRs, size=nChains), axis=1)

    def _decide(self, currentLogPs, proposalLogPs, nChains):
        """
        makes a decision about whether the proposed vector should be accepted
        """
        logMetropRatio = proposalLogPs - currentLogPs
        decision = log(random.uniform(size=nChains)) < logMetropRatio
        return decision


class DreamChain(MCMC):
    """
    DreamChain uses a special step method DreamStepper for stepping. It also allows the object controlling it to control
    the looping, proposing and rejecting, which is not possible with other MCMC objects. This allows the chains to be 
    interdependent.
    
    The MCMC._loop() function has been split up into several functions, so that both DREAM and other step methods can be 
    use simultaneously but it is not currently set up to do so, so only DREAM will work right now.
    """
    DREAMstepper = None
    _DREAM_dimensions = 0
    _DREAM_slices = {}

    def __init__(self, DREAMc_container, input=None, DREAM_variables=None, db='ram', name='MCMC', calc_deviance=True, **kwds):
        """Initialize an MCMC instance.

        :Parameters:
          - input : module, list, tuple, dictionary, set, object or nothing.
              Model definition, in terms of Stochastics, Deterministics, Potentials and Containers.
              If nothing, all nodes are collected from the base namespace.
          - db : string
              The name of the database backend that will store the values
              of the stochastics and deterministics sampled during the MCMC loop.
          - verbose : integer
              Level of output verbosity: 0=none, 1=low, 2=medium, 3=high
          - **kwds :
              Keywords arguments to be passed to the database instantiation method.
        """
        MCMC.__init__(self, input=input, db=db, name=name, calc_deviance=calc_deviance, **kwds)
        self.use_step_method(DreamStepper, input, DREAMc_container)

    def dimension(self):
        """Compute the dimension of the sampling space and identify the slices
        belonging to each stochastic.
        """
        self._DREAM_dimensions = 0
        self._DREAM_slices = {}
        for stochastic in self._DREAM_variables:
            if isinstance(stochastic.value, np.matrix):
                p_len = len(stochastic.value.A.ravel())
            elif isinstance(stochastic.value, np.ndarray):
                p_len = len(stochastic.value.ravel())
            else:
                p_len = 1
            self._slices[stochastic] = slice(self._DREAM_dimensions, self._DREAM_dimensions + p_len)
            self._DREAM_dimensions += p_len

    def sampleInit(self, iter, burn=0, thin=1, tune_interval=1000, tune_throughout=True, save_interval=None, verbose=0):
        """
        sample(iter, burn, thin, tune_interval, tune_throughout, save_interval, verbose)

        Initialize traces, run sampling loop, clean up afterward. Calls _loop.

        :Parameters:
          - iter : int
            Total number of iterations to do
          - burn : int
            Variables will not be tallied until this many iterations are complete, default 0
          - thin : int
            Variables will be tallied at intervals of this many iterations, default 1
          - tune_interval : int
            Step methods will be tuned at intervals of this many iterations, default 1000
          - tune_throughout : boolean
            If true, tuning will continue after the burnin period (True); otherwise tuning
            will halt at the end of the burnin period.
          - save_interval : int or None
            If given, the model state will be saved at intervals of this many iterations
          - verbose : boolean
        """
        self.assign_step_methods()
        for step_method in self.step_methods:
            if type(step_method) == DreamStepper:
                self.DREAMstepper = step_method

        if burn >= iter:
            raise ValueError, 'Burn interval must be smaller than specified number of iterations.'
        self._iter = int(iter)
        self._burn = int(burn)
        self._thin = int(thin)
        self._tune_interval = int(tune_interval)
        self._tune_throughout = tune_throughout
        self._save_interval = save_interval
        length = int(np.ceil((1.0 * iter - burn) / thin))
        self.max_trace_length = length
        self._tuning = True
        self._tuned_count = 0
        self._cur_trace_index = 0
        self.max_trace_length = iter
        self._iter = iter
        if verbose > 0:
            self.verbose = verbose
        self.seed()
        if length is None:
            length = iter
        self.db._initialize(self._funs_to_tally, length)
        for v in self._variables_to_tally:
            v.trace = self.db._traces[v.__name__]

        self._current_iter = 0
        self.status = 'running'
        start = time.time()
        return

    def initStep(self, _current_iter):
        self._current_iter = _current_iter
        if self.status == 'paused':
            return
        i = self._current_iter
        if i and not i % self._tune_interval and self._tuning:
            self.tune()
        if i == self._burn:
            if self.verbose > 0:
                print 'Burn-in interval complete'
            if not self._tune_throughout:
                if self.verbose > 0:
                    print 'Stopping tuning due to burn-in being complete.'
                self._tuning = False

    def continueStep(self):
        i = self._current_iter
        for step_method in self.step_methods:
            if step_method != DREAMstepper:
                if self.verbose > 2:
                    print 'Step method %s stepping' % step_method._id
                step_method.step()

        if i % self._thin == 0 and i >= self._burn:
            self.tally()
        if self._save_interval is not None:
            if i % self._save_interval == 0:
                self.save_state()
        if not i % 10000 and i and self.verbose > 0:
            per_step = (time.time() - start) / i
            remaining = self._iter - i
            time_left = remaining * per_step
            print 'Iteration %i of %i (%i:%02d:%02d remaining)' % (i, self._iter, time_left / 3600, time_left % 3600 / 60, time_left % 60)
        if not i % 1000:
            self.commit()
        self._current_iter += 1
        return

    def propose(self, proposalVector, current_iter):
        if self.verbose > 2:
            print 'Step method %s stepping' % step_method._id
        self.DREAMstepper.propose(proposalVector)

    def currentVector(self):
        return self.DREAMstepper.currentVector()

    def logp(self):
        return self.DREAMstepper.logp_plus_loglike

    def reject(self):
        self.DREAMstepper.reject()

    def sampleFinalize(self):
        self._finalize()


class DreamStepper(StepMethod):
    _DREAM_dimensions = 0
    _DREAM_slices = {}

    def __init__(self, stochastics, DREAM_container, verbose=0, tally=True):
        self._DREAM_container = DREAM_container
        StepMethod.__init__(self, stochastics, tally=tally)
        if verbose is not None:
            self.verbose = verbose
        else:
            self.verbose = stochastic.verbose
        self.dimension()
        return

    def dimension(self):
        """Compute the dimension of the sampling space and identify the slices
        belonging to each stochastic.
        """
        self._DREAM_dimensions = 0
        self._DREAM_slices = {}
        for stochastic in self.stochastics:
            if isinstance(stochastic.value, np.matrix):
                p_len = len(stochastic.value.A.ravel())
            elif isinstance(stochastic.value, np.ndarray):
                p_len = len(stochastic.value.ravel())
            else:
                p_len = 1
            self._DREAM_slices[stochastic] = slice(self._DREAM_dimensions, self._DREAM_dimensions + p_len)
            self._DREAM_dimensions += p_len

    def currentVector(self):
        currentVector = zeros(self._DREAM_dimensions)
        for stochastic in self.stochastics:
            value = 0
            if isinstance(stochastic.value, np.matrix):
                value = stochastic.value.A.ravel()
            elif isinstance(stochastic.value, np.ndarray):
                value = stochastic.value.ravel()
            else:
                value = stochastic.value
            currentVector[self._DREAM_slices[stochastic]] = value

        return currentVector

    def propose(self, proposalVector):
        for stochastic in self.stochastics:
            proposedValue = proposalVector[self._DREAM_slices[stochastic]]
            if iterable(stochastic.value):
                proposedValue = np.reshape(proposalVector[self._DREAM_slices[stochastic]], np.shape(stochastic.value))
            stochastic.value = proposedValue

    def reject(self):
        for stochastic in self.stochastics:
            stochastic.revert()


class GRConvergence():
    """
    Gelman Rubin convergence diagnostic calculator class.
    """
    _R = Inf

    def __init__(self):
        pass

    def _get_R(self):
        return self._R

    R = property(_get_R)

    def update(self, sequences, burnIn, n, dimensions, nChains):
        start = burnIn + (n - burnIn) * 0.5
        end = n
        N = end - start
        sequences = sequences[:, :, start:end]
        variances = var(sequences, axis=2)
        means = mean(sequences, axis=2)
        withinChainVariances = mean(variances, axis=0)
        betweenChainVariances = var(means, axis=0) * N
        varEstimate = (1 - 1.0 / N) * withinChainVariances + 1.0 / N * betweenChainVariances
        self._R = sqrt(varEstimate / withinChainVariances)