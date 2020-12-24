# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gleipnir/dnest4.py
# Compiled at: 2019-07-02 15:48:17
# Size of source mod 2**32: 13860 bytes
"""Implementation on top of DNest4 via its python bindings.

This module defines the class for Nested Sampling using using the DNest4
program via its Python bindings. Note that DNest4 and its Python bindings have
to be built and installed separately (from gleipnir) before this module can be
used.

DNest4: https://github.com/eggplantbren/DNest4

References:
    1. Brewer, B., & Foreman-Mackey, D. (2018). DNest4: Diffusive Nested
        1 - 33. doi:http://dx.doi.org/10.18637/jss.v086.i07
        Sampling in C++ and Python. Journal of Statistical Software, 86(7),
    2. Brewer, B. J., Pártay, L. B., & Csányi, G. (2011). Diffusive nested
        sampling. Statistics and Computing, 21(4), 649-656

"""
import numpy as np, pandas as pd, warnings
from .nsbase import NestedSamplingBase
try:
    import dnest4
except ImportError as err:
    raise err

class _DNest4Model(object):
    __doc__ = 'Model class for use with the Python interface to DNest4.\n    Design based on the model class from the DNest4/python gaussian example:\n    https://github.com/eggplantbren/DNest4/blob/master/python/examples/gaussian/gaussian.py\n    '

    def __init__(self, log_likelihood_func, from_prior_func, widths, centers):
        """Initialize the DNest4 model.
        Args:
            log_likelihood_func (function): The loglikelihood function to use
                during the Nested Sampling run.
            from_prior_func (function): The function to use when randomly
                selecting parameter vectors from the prior space.
            widths (numpy.array): The approximate widths of the prior
                distrbutions.
            centers (numpy.array): The approximate center points of the prior
                distributions.
        """
        self._log_likelihood = log_likelihood_func
        self._from_prior = from_prior_func
        self._widths = widths
        self._centers = centers
        self._n_dim = len(widths)

    def log_likelihood(self, coords):
        """The model's log_likelihood function"""
        return self._log_likelihood(coords)

    def from_prior(self):
        """The model's function to select random points from the prior space."""
        return self._from_prior()

    def perturb(self, coords):
        """The perturb function to perform Monte Carlo trial moves."""
        idx = np.random.randint(self._n_dim)
        coords[idx] += self._widths[idx] * (np.random.uniform(size=1) - 0.5)
        cw = self._widths[idx]
        cc = self._centers[idx]
        coords[idx] = dnest4.wrap(coords[idx], cc - 0.5 * cw, cc + 0.5 * cw)
        return 0.0


class DNest4NestedSampling(NestedSamplingBase):
    __doc__ = "Nested Sampling using DNest4.\n    DNest4: https://github.com/eggplantbren/DNest4\n\n    Attributes:\n        sampled_parameters (list of :obj:gleipnir.sampled_parameter.SampledParameter):\n            The parameters that are being sampled during the Nested Sampling\n            run.\n        loglikelihood (function): The log-likelihood function to use for\n            assigning a likelihood to parameter vectors during the sampling.\n        population_size (int): The number of points to use in the Nested\n            Sampling active population.\n        n_diffusive_levels (int, optional): The max number of diffusive likelihood\n            levels that DNest4 should initial during the Diffusive Nested\n            Sampling run. Default: 20\n        dnest4_backend (str, optional): The python DNest4 backend for storing\n            the output. Options are: 'memory' and 'csv'. If 'memory' the\n            DNest4 outputs are stored in memory during the run. If 'csv' the\n            DNest4 outputs are written out to filse with a CSV format during\n            the run. Defualt: 'memory'.\n            dnest4_kwargs: Any additional DNest4 keyword arguments to be passed\n                to the DNest4 sampler. The available options are:\n                num_steps (int): The number of MCMC iterations to run. If None,\n                    will run forever.\n                    Default: None\n                new_level_interval (int): The number of moves to run before\n                    creating a new diffusive likelihood level. Default: 10000\n                lam (float): Set the backtracking scale length. Default: 5.0\n                beta (float): Set the strength of effect to force the histogram\n                    to equal bin counts. Default: 100\n\n\n    References:\n        1. Brewer, B., & Foreman-Mackey, D. (2018). DNest4: Diffusive Nested\n            1 - 33. doi:http://dx.doi.org/10.18637/jss.v086.i07\n            Sampling in C++ and Python. Journal of Statistical Software, 86(7),\n        2. Brewer, B. J., Pártay, L. B., & Csányi, G. (2011). Diffusive nested\n            sampling. Statistics and Computing, 21(4), 649-656\n    "

    def __init__(self, sampled_parameters, loglikelihood, population_size, n_diffusive_levels=20, dnest4_backend='memory', **dnest4_kwargs):
        """Initialize the DNest4 Nested Sampler."""
        self.sampled_parameters = sampled_parameters
        self.loglikelihood = loglikelihood
        self.population_size = population_size
        self.dnest4_backend = dnest4_backend
        self.n_diffusive_levels = n_diffusive_levels
        self.dnest4_kwargs = dnest4_kwargs
        self._n_dims = len(sampled_parameters)
        self._file_root = './dnest4_run_'
        self._log_evidence = None
        self._information = None
        self._output = None
        self._post_eval = False
        if 'num_steps' not in list(self.dnest4_kwargs.keys()):
            self.dnest4_kwargs['num_steps'] = 1000

        def from_prior():
            return np.array([sampled_parameter.rvs(1)[0] for sampled_parameter in self.sampled_parameters])

        self._from_prior = from_prior
        widths = []
        centers = []
        for sampled_parameter in sampled_parameters:
            rv = sampled_parameter.rvs(10000)
            low = rv.min()
            high = rv.max()
            width = high - low
            center = (high + low) / 2.0
            widths.append(width)
            centers.append(center)

        widths = np.array(widths)
        centers = np.array(centers)
        self._widths = widths
        self._centers = centers
        self._dnest4_model = _DNest4Model(loglikelihood, self._from_prior, widths, centers)

    def run(self, verbose=False):
        """Initiate the DNest4 Nested Sampling run."""
        if self.dnest4_backend == 'csv':
            backend = dnest4.backends.CSVBackend('./dnest4_run_', sep=' ')
        else:
            backend = dnest4.backends.MemoryBackend()
        sampler = dnest4.DNest4Sampler((self._dnest4_model), backend=backend)
        output = (sampler.sample)(self.n_diffusive_levels, num_particles=self.population_size, **self.dnest4_kwargs)
        self._output = output
        for i, sample in enumerate(output):
            if verbose and (i + 1) % 100 == 0:
                stats = sampler.postprocess()
                print('Iteration: {0} log(Z): {1}'.format(i + 1, stats['log_Z']))

        stats = sampler.postprocess(resample=1)
        self._log_evidence = stats['log_Z']
        self._information = stats['H']
        logZ_err = np.sqrt(self._information / self.population_size)
        self._logZ_err = logZ_err
        ev_err = np.exp(logZ_err)
        self._evidence_error = ev_err
        self._evidence = np.exp(self._log_evidence)
        self._samples = np.array(sampler.backend.posterior_samples)
        print(len(sampler.backend.samples[(-1)]))
        print(len(sampler.backend.weights[(-1)]))
        self._last_live_sample = sampler.backend.samples[(-1)]
        self._last_live_sample_weights = sampler.backend.weights[(-1)]
        self._last_live_sample_info = pd.DataFrame(sampler.backend.sample_info[(-1)])
        return (self.log_evidence, self.log_evidence_error)

    @property
    def evidence(self):
        """float: Estimate of the Bayesian evidence, or Z."""
        return self._evidence

    @evidence.setter
    def evidence(self, value):
        warnings.warn('evidence is not settable')

    @property
    def evidence_error(self):
        """float: Estimate (rough) of the error in the evidence, or Z.

        The error in the evidence is computed as the approximation:
            exp(sqrt(information/population_size))
        """
        return self._evidence_error

    @evidence_error.setter
    def evidence_error(self, value):
        warnings.warn('evidence_error is not settable')

    @property
    def log_evidence(self):
        """float: Estimate of the natural logarithm of the Bayesian evidence, or ln(Z).
        """
        return self._log_evidence

    @log_evidence.setter
    def log_evidence(self, value):
        warnings.warn('log_evidence is not settable')

    @property
    def log_evidence_error(self):
        """float: Estimate of the error in the natural logarithm of the evidence.
        """
        return self._logZ_err

    @log_evidence_error.setter
    def log_evidence_error(self, value):
        warnings.warn('log_evidence_error is not settable')

    @property
    def information(self):
        """float: Estimate of the Bayesian information, or H."""
        return self._information

    @information.setter
    def information(self, value):
        warnings.warn('information is not settable')

    @property
    def dnest4_file_root(self):
        """str: The file root used by Polychord output files."""
        return self._file_root

    @dnest4_file_root.setter
    def dnest4_file_root(self, value):
        self._file_root = value

    def posteriors(self, nbins=None):
        """Estimates of the posterior marginal probability distributions of each parameter.
        Returns:
            dict of tuple of (numpy.ndarray, numpy.ndarray, numpy.ndarray): The
                histogram estimates of the posterior marginal probability
                distributions. The returned dict is keyed by the sampled
                parameter names and each element is a tuple with
                (marginal_weights, bin_edges, bin_centers).
        """
        if not self._post_eval:
            samples = self._samples
            if nbins is None:
                nbins = 2 * int(np.cbrt(len(samples)))
            nd = samples.shape[1]
            self._posteriors = dict()
            for ii in range(nd):
                marginal, edge = np.histogram((samples[:, ii]), density=True, bins=nbins)
                center = (edge[:-1] + edge[1:]) / 2.0
                self._posteriors[self.sampled_parameters[ii].name] = (marginal, edge, center)

            self._post_eval = True
        return self._posteriors

    def max_loglikelihood(self):
        mx = self._last_live_sample_info.max()
        ml = mx['log_likelihood']
        return ml

    def deviance_ic(self):
        """Estimate Deviance Information Criterion.
        This function estimates the Deviance Information Criterion (DIC) for the
        model simulated with Nested Sampling (NS). It does so by using the
        posterior distribution estimates computed from the NS outputs.
        The DIC formula is given by:
            DIC = p_D + D_bar,
        where p_D = D_bar - D(theta_bar), D_bar is the posterior average of
        the deviance D(theta)= -2*ln(L(theta)) with L(theta) the likelihood
        of parameter set theta, and theta_bar is posterior average parameter set.

        Returns:
            float: The DIC estimate.
        """
        params = self._last_live_sample
        log_likelihoods = self._last_live_sample_info['log_likelihood']
        weights = self._last_live_sample_weights
        D_of_theta = -2.0 * log_likelihoods
        D_bar = np.average(D_of_theta, weights=weights)
        print(D_bar)
        theta_bar = np.average(params, axis=0, weights=weights)
        print(theta_bar)
        D_of_theta_bar = -2.0 * self.loglikelihood(theta_bar)
        p_D = D_bar - D_of_theta_bar
        return p_D + D_bar

    def best_fit_likelihood(self):
        """Parameter vector with the maximum likelihood.
        Returns:
            numpy.array: The parameter vector.
        """
        midx = np.argmax(self._last_live_sample_info['log_likelihood'].values)
        ml = self._last_live_sample[midx]
        return ml