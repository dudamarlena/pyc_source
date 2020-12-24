# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zeus/zeus.py
# Compiled at: 2020-04-30 07:04:05
# Size of source mod 2**32: 18794 bytes
import numpy as np
from itertools import permutations
import random
from tqdm import tqdm
import logging
from .samples import samples
from .fwrapper import _FunctionWrapper
from .autocorr import _autocorr_time

class sampler:
    __doc__ = "\n    An Ensemble Slice MCMC sampler.\n    arXiv:2002.06212\n\n    Args:\n        nwalkers (int): The number of walkers in the ensemble.\n        ndim (int): The number of dimensions/parameters.\n        logprob_fn (callable): A python function that takes a vector in the\n            parameter space as input and returns the natural logarithm of the\n            unnormalised posterior probability at that position.\n        args (list): Extra arguments to be passed into the logp.\n        kwargs (list): Extra arguments to be passed into the logp.\n        proposal (dict): Dictionary containing the probability of each proposal (Default is {'differential' : 1.0, 'gaussian' : 0.0, 'jump' : 0.0, 'random' : 0.0}).\n        tune (bool): Tune the scale factor to optimize performance (Default is True.)\n        tolerance (float): Tuning optimization tolerance (Default is 0.05).\n        patience (int): Number of tuning steps to wait to make sure that tuning is done (Default is 5).\n        maxsteps (int): Number of maximum stepping-out steps (Default is 10^4).\n        mu (float): Scale factor (Default value is 1.0), this will be tuned if tune=True.\n        maxiter (int): Number of maximum Expansions/Contractions (Default is 10^4).\n        pool (bool): External pool of workers to distribute workload to multiple CPUs (default is None).\n        vectorize (bool): If true (default is False), logprob_fn receives not just one point but an array of points, and returns an array of likelihoods.\n        verbose (bool): If True (default) print log statements.\n    "

    def __init__(self, nwalkers, ndim, logprob_fn, args=None, kwargs=None, proposal={'differential':1.0, 
 'gaussian':0.0,  'jump':0.0,  'random':0.0}, tune=True, tolerance=0.05, patience=5, maxsteps=10000, mu=1.0, maxiter=10000, pool=None, vectorize=False, verbose=True):
        self.logger = logging.getLogger()
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        handler = logging.StreamHandler()
        self.logger.addHandler(handler)
        if verbose:
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.WARNING)
        self.logprob_fn = _FunctionWrapper(logprob_fn, args, kwargs)
        self.nwalkers = int(nwalkers)
        self.ndim = int(ndim)
        if self.nwalkers < 2 * self.ndim:
            raise ValueError('Please provide at least (2 * ndim) walkers.')
        else:
            if self.nwalkers % 2 == 1:
                raise ValueError('Please provide an even number of walkers.')
            else:
                self.mu = mu
                self.mus = []
                self.mus.append(self.mu)
                self.tune = tune
                self.maxsteps = maxsteps
                self.patience = patience
                self.tolerance = tolerance
                self.maxiter = maxiter
                self.pool = pool
                self.vectorize = vectorize
                self.samples = samples(self.ndim, self.nwalkers)
                self.proposal = proposal
                if 'differential' not in self.proposal:
                    if 'gaussian' not in self.proposal:
                        if 'jump' not in self.proposal and 'random' not in self.proposal:
                            raise ValueError('Please provide at least one of the following proposals: differential, gaussian, jump, and random.')
            total = 0.0
            for key in self.proposal:
                if not self.proposal[key] < 0.0:
                    if self.proposal[key] > 1.0:
                        raise ValueError('Please provide a dictionary with the probability of each proposal in the range [0,1].')
                    if key not in ('differential', 'gaussian', 'jump', 'random'):
                        raise ValueError('Proposal not recognised! Please provide a valid proposal (i.e. differential, gaussian, jump, or random).')
                    total += self.proposal[key]

            if round(total, 4) != 1.0:
                raise ValueError('The total probability of all proposals must be equal to 1.0.')

    def run(self, start, nsteps=1000, thin=1, progress=True):
        """
        Calling this method runs the mcmc sampler.

        Args:
            start (float) : Starting point for the walkers.
            nsteps (int): Number of steps/generations (default is 1000).
            thin (float): Thin the chain by this number (default is 1 no thinning).
            progress (bool): If True (default), show progress bar (requires tqdm).
        """
        if self.pool is None:
            distribute = map
        else:
            distribute = self.pool.map
        if self.vectorize:
            distribute = lambda func, x: func(x)
        logging.info('Initialising ensemble of %d walkers...', self.nwalkers)
        if np.shape(start) != (self.nwalkers, self.ndim):
            raise ValueError('Incompatible input dimensions! \nPlease provide array of shape (nwalkers, ndim) as the starting position.')
        X = np.copy(start)
        Z = np.asarray(list(distribute(self.logprob_fn, X)))
        if not np.all(np.isfinite(Z)):
            raise ValueError('Invalid walker initial positions! \nInitialise walkers from positions of finite log probability.')
        batch = list(np.arange(self.nwalkers))
        self.nsteps = int(nsteps)
        self.thin = int(thin)
        self.samples.extend(self.nsteps // self.thin)
        self.neval = np.zeros(self.nsteps)
        ncount = 0
        if progress:
            t = tqdm(total=nsteps, desc='Sampling progress : ')
        for i in range(self.nsteps):
            nexp = 0
            ncon = 0
            if self.tune:
                move = max((self.proposal), key=(self.proposal.get))
            else:
                move = np.random.choice((list(self.proposal.keys())), p=(list(self.proposal.values())))
            np.random.shuffle(batch)
            batch0 = batch[:int(self.nwalkers / 2)]
            batch1 = batch[int(self.nwalkers / 2):]
            sets = [[batch0, batch1], [batch1, batch0]]
            for ensembles in sets:
                indeces = np.arange(int(self.nwalkers / 2))
                active, inactive = ensembles
                if move == 'differential':
                    perms = list(permutations(inactive, 2))
                    pairs = np.asarray(random.sample(perms, int(self.nwalkers / 2))).T
                    directions = self.mu * (X[pairs[0]] - X[pairs[1]])
                else:
                    if move == 'gaussian':
                        mean = np.mean((X[inactive]), axis=0)
                        cov = np.cov((X[inactive]), rowvar=False)
                        directions = self.mu * np.random.multivariate_normal(mean, cov, size=(int(self.nwalkers / 2)))
                    else:
                        if move == 'jump':
                            perms = list(permutations(inactive, 2))
                            pairs = np.asarray(random.sample(perms, int(self.nwalkers / 2))).T
                            directions = 2.0 * (X[pairs[0]] - X[pairs[1]])
                        else:
                            if move == 'random':
                                directions = np.random.normal(0.0, 1.0, size=(int(self.nwalkers / 2), self.ndim))
                                directions /= np.linalg.norm(directions, axis=0)
                                directions *= self.mu
                            Z0 = Z[active] - np.random.exponential(size=(int(self.nwalkers / 2)))
                            L = -np.random.uniform(0.0, 1.0, size=(int(self.nwalkers / 2)))
                            R = L + 1.0
                            J = np.floor(self.maxsteps * np.random.uniform(0.0, 1.0, size=(int(self.nwalkers / 2))))
                            K = self.maxsteps - 1 - J
                            ncall = 0
                            mask_J = np.full(int(self.nwalkers / 2), True)
                            Z_L = np.empty(int(self.nwalkers / 2))
                            X_L = np.empty((int(self.nwalkers / 2), self.ndim))
                            cnt = 0
                            while len(mask_J[mask_J]) > 0:
                                for j in indeces[mask_J]:
                                    if J[j] < 1:
                                        mask_J[j] = False

                                X_L[mask_J] = directions[mask_J] * L[mask_J][:, np.newaxis] + X[active][mask_J]
                                Z_L[mask_J] = np.asarray(list(distribute(self.logprob_fn, X_L[mask_J])))
                                for j in indeces[mask_J]:
                                    ncall += 1
                                    if Z0[j] < Z_L[j]:
                                        L[j] = L[j] - 1.0
                                        J[j] = J[j] - 1
                                        nexp += 1
                                    else:
                                        mask_J[j] = False

                                cnt += 1
                                if cnt > self.maxiter:
                                    raise RuntimeError('Number of expansions exceeded maximum limit! \nMake sure that the pdf is well-defined. \nOtherwise increase the maximum limit (maxiter=10^4 by default).')

                            mask_K = np.full(int(self.nwalkers / 2), True)
                            Z_R = np.empty(int(self.nwalkers / 2))
                            X_R = np.empty((int(self.nwalkers / 2), self.ndim))
                            cnt = 0
                            while len(mask_K[mask_K]) > 0:
                                for j in indeces[mask_K]:
                                    if K[j] < 1:
                                        mask_K[j] = False

                                X_R[mask_K] = directions[mask_K] * R[mask_K][:, np.newaxis] + X[active][mask_K]
                                Z_R[mask_K] = np.asarray(list(distribute(self.logprob_fn, X_R[mask_K])))
                                for j in indeces[mask_K]:
                                    ncall += 1
                                    if Z0[j] < Z_R[j]:
                                        R[j] = R[j] + 1.0
                                        K[j] = K[j] - 1
                                        nexp += 1
                                    else:
                                        mask_K[j] = False

                                cnt += 1
                                if cnt > self.maxiter:
                                    raise RuntimeError('Number of expansions exceeded maximum limit! \nMake sure that the pdf is well-defined. \nOtherwise increase the maximum limit (maxiter=10^4 by default).')

                            Widths = np.empty(int(self.nwalkers / 2))
                            Z_prime = np.empty(int(self.nwalkers / 2))
                            X_prime = np.empty((int(self.nwalkers / 2), self.ndim))
                            mask = np.full(int(self.nwalkers / 2), True)
                            cnt = 0
                            while len(mask[mask]) > 0:
                                Widths[mask] = L[mask] + np.random.uniform(0.0, 1.0, size=(len(mask[mask]))) * (R[mask] - L[mask])
                                X_prime[mask] = directions[mask] * Widths[mask][:, np.newaxis] + X[active][mask]
                                Z_prime[mask] = np.asarray(list(distribute(self.logprob_fn, X_prime[mask])))
                                ncall += len(mask[mask])
                                for j in indeces[mask]:
                                    if Z0[j] < Z_prime[j]:
                                        mask[j] = False
                                    else:
                                        if Widths[j] < 0.0:
                                            L[j] = Widths[j]
                                            ncon += 1

                                cnt += 1
                                if cnt > self.maxiter:
                                    raise RuntimeError('Number of contractions exceeded maximum limit! \nMake sure that the pdf is well-defined. \nOtherwise increase the maximum limit (maxiter=10^4 by default).')

                            X[active] = X_prime
                            Z[active] = Z_prime
                            self.neval[i] += ncall

            if self.tune:
                nexp = max(1, nexp)
                self.mu *= 2.0 * nexp / (nexp + ncon)
                self.mus.append(self.mu)
                if np.abs(nexp / (nexp + ncon) - 0.5) < self.tolerance:
                    ncount += 1
                if ncount > self.patience:
                    self.tune = False
                if (i + 1) % self.thin == 0:
                    self.samples.save(X, Z)
                if progress:
                    t.update()

        if progress:
            t.close()

    def reset(self):
        """
        Reset the state of the sampler. Delete any samples stored in memory.
        """
        self.samples = samples(self.ndim, self.nwalkers)

    @property
    def chain(self):
        """
        Returns the chains.

        Returns:
            Returns the chains of shape (nwalkers, nsteps, ndim).
        """
        return self.samples.chain

    def flatten(self, discard=0, thin=1):
        """
        Flatten the chain.

        Args:
            discard (int): The number of burn-in steps to remove from each walker (default is 0).
            thin (int): The ammount to thin the chain (default is 1, no thinning).

        Returns:
            2D Flattened chain.
        """
        return self.samples.flatten(discard, thin)

    @property
    def autocorr_time(self):
        """
        Integrated Autocorrelation Time (IAT) of the Markov Chain.

        Returns:
            Array with the IAT of each parameter.
        """
        return _autocorr_time(np.swapaxes(self.chain[int(self.nsteps / (self.thin * 2.0)):, :, :], 0, 1))

    @property
    def ess(self):
        """
        Effective Sampling Size (ESS) of the Markov Chain.

        Returns:
            ESS
        """
        return self.nwalkers * self.samples.length / np.mean(self.autocorr_time)

    @property
    def ncall(self):
        """
        Number of Log Prob calls.

        Returns:
            ncall
        """
        return np.sum(self.neval)

    @property
    def efficiency(self):
        """
        Effective Samples per Log Probability Evaluation.

        Returns:
            efficiency
        """
        return self.ess / self.ncall

    @property
    def scale_factor(self):
        """
        Scale factor values during tuning.

        Returns:
            scale factor mu
        """
        return np.asarray(self.mus)

    @property
    def summary(self):
        """
        Summary of the MCMC run.
        """
        logging.info('Summary')
        logging.info('-------')
        logging.info('Number of Generations: ' + str(self.samples.length))
        logging.info('Number of Parameters: ' + str(self.ndim))
        logging.info('Number of Walkers: ' + str(self.nwalkers))
        logging.info('Number of Tuning Generations: ' + str(len(self.mus)))
        logging.info('Scale Factor: ' + str(round(self.mu, 6)))
        logging.info('Mean Integrated Autocorrelation Time: ' + str(round(np.mean(self.autocorr_time), 2)))
        logging.info('Effective Sample Size: ' + str(round(self.ess, 2)))
        logging.info('Number of Log Probability Evaluations: ' + str(self.ncall))
        logging.info('Effective Samples per Log Probability Evaluation: ' + str(round(self.efficiency, 6)))
        if self.thin > 1:
            logging.info('Thinning rate: ' + str(self.thin))

    def get_chain(self, flat=False, thin=1, discard=0):
        """
        Get the Markov chain containing the samples.

        Args:
            flat (bool) : If True then flatten the chain into a 2D array by combining all walkers (default is False).
            thin (int) : Thinning parameter (the default value is 1).
            discard (int) : Number of burn-in steps to be removed from each walker (default is 0).

        Returns:
            Array object containg the Markov chain samples (2D if flat=True, 3D if flat=False).
        """
        if flat:
            return self.flatten(discard=discard, thin=thin)
        return self.chain[discard::thin, :, :]

    def get_log_prob(self, flat=False, thin=1, discard=0):
        """
        Get the value of the log probability function evalutated at the samples of the Markov chain.

        Args:
            flat (bool) : If True then flatten the chain into a 1D array by combining all walkers (default is False).
            thin (int) : Thinning parameter (the default value is 1).
            discard (int) : Number of burn-in steps to be removed from each walker (default is 0).

        Returns:
            Array containing the value of the log probability at the samples of the Markov chain (1D if flat=True, 2D otherwise).
        """
        if flat:
            return self.samples.flatten_logprob(discard=discard, thin=thin)
        return self.samples.logprob[discard::thin, :]

    @property
    def get_last_sample(self):
        """
            Return the last position of the walkers.
        """
        return self.chain[(-1)]

    def run_mcmc(self, *args, **kwargs):
        """
        Wrapper for run method.
        """
        return (self.run)(*args, **kwargs)