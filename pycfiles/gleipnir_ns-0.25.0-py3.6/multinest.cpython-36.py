# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gleipnir/multinest.py
# Compiled at: 2019-07-02 15:48:17
# Size of source mod 2**32: 12430 bytes
"""Implementation on top of MultiNest via PyMultiNest.

This module defines the class for Nested Sampling using the MultiNest
program via its Python wrapper PyMultiNest. Note that PyMultiNest and MultiNest
have to be built and installed separately (from gleipnir) before this module
can be used.

PyMultiNest: https://github.com/JohannesBuchner/PyMultiNest
MultiNest: https://github.com/JohannesBuchner/MultiNest

References:
    MultiNest:
    1. Feroz, Farhan, and M. P. Hobson. "Multimodal nested sampling: an
        efficient and robust alternative to Markov Chain Monte Carlo
        methods for astronomical data analyses." Monthly Notices of the
        Royal Astronomical Society 384.2 (2008): 449-463.
    2. Feroz, F., M. P. Hobson, and M. Bridges. "MultiNest: an efficient
        and robust Bayesian inference tool for cosmology and particle
        physics." Monthly Notices of the Royal Astronomical Society 398.4
        (2009): 1601-1614.
    3. Feroz, F., et al. "Importance nested sampling and the MultiNest
        algorithm." arXiv preprint arXiv:1306.2144 (2013).
    PyMultiNest:
    4. Buchner, J., et al. "X-ray spectral modelling of the AGN obscuring
        region in the CDFS: Bayesian model selection and catalogue."
        Astronomy & Astrophysics 564 (2014): A125.

"""
import numpy as np, warnings
from .nsbase import NestedSamplingBase
try:
    import pymultinest
    from pymultinest.solve import solve
    from pymultinest.analyse import Analyzer
except ImportError as err:
    raise err

class MultiNestNestedSampling(NestedSamplingBase):
    __doc__ = 'Nested Sampling using MultiNest.\n    PyMultiNest: https://github.com/JohannesBuchner/PyMultiNest\n    MultiNest: https://github.com/JohannesBuchner/MultiNest\n\n    Attributes:\n        sampled_parameters (list of :obj:gleipnir.sampled_parameter.SampledParameter):\n            The parameters that are being sampled during the Nested Sampling\n            run.\n        loglikelihood (function): The log-likelihood function to use for\n            assigning a likelihood to parameter vectors during the sampling.\n        population_size (int): The number of points to use in the Nested\n            Sampling active population.\n        multinest_kwargs (dict): Additional keyword arguments that should be\n            passed to the PyMultiNest MultiNest solver. Available options are:\n                importance_nested_sampling (bool): Should MultiNest use\n                    Importance Nested Sampling (INS). Default: True\n                constant_efficiency_mode (bool): Should MultiNest run in\n                    constant sampling efficiency mode. Default: False\n\t            sampling_efficiency (float): Set the MultiNest sampling\n                    efficiency. 0.3 is recommended for evidence evaluation,\n                    while 0.8 is recommended for parameter estimation.\n                    Default: 0.8\n                resume (bool): Resume from a previous MultiNest run (using\n                    the last saved checkpoint in the MultiNest output files).\n                    Default: True\n                write_output (bool): Specify whether MultiNest should write\n                    to output files. True is required for additional\n                    analysis. Default: True\n                multimodal (bool): Set whether MultiNest performs mode\n                    separation. Default: True\n                max_mode (int): Set the maximum number of modes allowed in\n                    mode separation (if multimodal=True). Default: 100\n                mode_tolerance (float): A lower bound for which MultiNest will\n                    use to separate mode samples and statistics with\n                    log-evidence value greater the given value.\n                    Default: -1e90\n                n_clustering_params (int): If multimodal=True, set the number\n                    of parameters to use in clustering during mode separation.\n                    If None, then MultiNest will use all the paramters for\n                    clustering during mode separation. If\n                    n<(number of sampled parameters), then MultiNest will only\n                    use a subset composed of the first n parameters for\n                    clustering during mode separation. Default: None\n                null_log_evidence (float): If multimodal=True, a lower bound\n                    for which MultiNest can use to separte mode samples and\n                    statistics with a local log-evidence value greater than the\n                    given bound. Default: -1.e90\n                log_zero (float): Set a threshold value for which points with\n                    a loglikelihood less than the given value will be ignored\n                    by MultiNest. Default: -1e100\n                max_iter (int): Set the maximum number of nested sampling\n                    iterations performed by MultiNest. If 0, then it is\n                    unlimited and MultiNest will stop using a different\n                    criterion. Default: 0\n\n\n    References:\n        1. Feroz, Farhan, and M. P. Hobson. "Multimodal nested sampling: an\n            efficient and robust alternative to Markov Chain Monte Carlo\n            methods for astronomical data analyses." Monthly Notices of the\n            Royal Astronomical Society 384.2 (2008): 449-463.\n        2. Feroz, F., M. P. Hobson, and M. Bridges. "MultiNest: an efficient\n            and robust Bayesian inference tool for cosmology and particle\n            physics." Monthly Notices of the Royal Astronomical Society 398.4\n            (2009): 1601-1614.\n        3. Feroz, F., et al. "Importance nested sampling and the MultiNest\n            algorithm." arXiv preprint arXiv:1306.2144 (2013).\n        4. Buchner, J., et al. "X-ray spectral modelling of the AGN obscuring\n            region in the CDFS: Bayesian model selection and catalogue."\n            Astronomy & Astrophysics 564 (2014): A125.\n    '

    def __init__(self, sampled_parameters, loglikelihood, population_size, **multinest_kwargs):
        """Initialize the MultiNest Nested Sampler."""
        self.sampled_parameters = sampled_parameters
        self.loglikelihood = loglikelihood
        self.population_size = population_size
        self.multinest_kwargs = multinest_kwargs
        self._nDims = len(sampled_parameters)
        self._nDerived = 0
        self._output = None
        self._post_eval = False

        def prior(hypercube):
            return np.array([self.sampled_parameters[i].invcdf(value) for i, value in enumerate(hypercube)])

        self._prior = prior
        self._file_root = 'multinest_run_'

    def run(self, verbose=False):
        """Initiate the MultiNest Nested Sampling run."""
        output = solve(LogLikelihood=self.loglikelihood, Prior=self._prior, n_dims=self._nDims, 
         n_live_points=self.population_size, 
         outputfiles_basename=self._file_root, 
         verbose=verbose, **self.multinest_kwargs)
        self._output = output
        return (self.log_evidence, self.log_evidence_error)

    @property
    def evidence(self):
        """float: Estimate of the Bayesian evidence, or Z."""
        return np.exp(self._output['logZ'])

    @evidence.setter
    def evidence(self, value):
        warnings.warn('evidence is not settable')

    @property
    def evidence_error(self):
        """float: Estimate (rough) of the error in the evidence, or Z."""
        return np.exp(self._output['logZerr'])

    @evidence_error.setter
    def evidence_error(self, value):
        warnings.warn('evidence_error is not settable')

    @property
    def log_evidence(self):
        """float: Estimate of the natural logarithm of the Bayesian evidence, or ln(Z).
        """
        return self._output['logZ']

    @log_evidence.setter
    def log_evidence(self, value):
        warnings.warn('log_evidence is not settable')

    @property
    def log_evidence_error(self):
        """float: Estimate of the error in the natural logarithm of the evidence.
        """
        return self._output['logZerr']

    @log_evidence_error.setter
    def log_evidence_error(self, value):
        warnings.warn('log_evidence_error is not settable')

    @property
    def information(self):
        """None: Not implemented yet->Estimate of the Bayesian information, or H."""
        pass

    @information.setter
    def information(self, value):
        warnings.warn('information is not settable')

    @property
    def multinest_file_root(self):
        """str. The root name used for MultNest output files."""
        return self._file_root

    @multinest_file_root.setter
    def multinest_file_root(self, value):
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
            samples = self._output['samples']
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
        mn_data = Analyzer((len(self.sampled_parameters)), (self._file_root), verbose=False).get_data()
        log_ls = -0.5 * mn_data[:, 1]
        ml = log_ls.max()
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
        mn_data = Analyzer((len(self.sampled_parameters)), (self._file_root), verbose=False).get_data()
        params = mn_data[:, 2:]
        log_likelihoods = -0.5 * mn_data[:, 1]
        prior_mass = mn_data[:, 0]
        norm_weights = prior_mass * np.exp(log_likelihoods) / self.evidence
        nw_mask = np.isnan(norm_weights)
        if np.any(nw_mask):
            return np.inf
        else:
            D_of_theta = -2.0 * log_likelihoods
            D_bar = np.average(D_of_theta, weights=norm_weights)
            theta_bar = np.average(params, axis=0, weights=norm_weights)
            D_of_theta_bar = -2.0 * self.loglikelihood(theta_bar)
            p_D = D_bar - D_of_theta_bar
            return p_D + D_bar

    def best_fit_likelihood(self):
        """Parameter vector with the maximum likelihood.
        Returns:
            numpy.array: The parameter vector.
        """
        mn_data = Analyzer((len(self.sampled_parameters)), (self._file_root), verbose=False).get_data()
        log_ls = -0.5 * mn_data[:, 1]
        midx = np.argmax(log_ls)
        ml = mn_data[midx][2:]
        return ml