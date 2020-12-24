# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gleipnir/dypolychord.py
# Compiled at: 2019-07-02 15:48:17
# Size of source mod 2**32: 12966 bytes
"""Implementation on top of dyPolyChord.

This module defines the class for Nested Sampling using using the dyPolyChord
program, which implements Dynamic Nested Sampling using PolyChord. Note that
dyPolyChord requires PolyChord (i.e., pypolychord), which
has to be built and installed separately (from gleipnir) before
this module can be used. dyPolyChord also requires nestcheck (installed
automatically if you pip install dyPolyChord) to post-process
the PolyChord outputs for dynamic Nested Sampling.

dyPolyChord: https://github.com/ejhigson/dyPolyChord
PolyChordLite/pypolychord: https://github.com/PolyChord/PolyChordLite
nestcheck:

References:
    dyPolyChord
    1. Higson, (2018). dyPolyChord: dynamic nested sampling with PolyChord.
        Journal of Open Source Software, 3(29), 965,
        https://doi.org/10.21105/joss.00965
    2. Higson, E., Handley, W., Hobson, M. et al. Dynamic nested sampling: an
        improved algorithm for parameter estimation and evidence calculation.
        Stat Comput (2018).
        https://doi.org/10.1007/s11222-018-9844-0
    PolyChord
    3. Handley, W. J., M. P. Hobson, and A. N. Lasenby. "PolyChord: nested
        sampling for cosmology." Monthly Notices of the Royal Astronomical
        Society: Letters 450.1 (2015): L61-L65.
    4. Handley, W. J., M. P. Hobson, and A. N. Lasenby. "POLYCHORD:
        next-generation nested sampling." Monthly Notices of the Royal
        Astronomical Society 453.4 (2015): 4384-4398.
    nestcheck
    5. Edward Higson, Will Handley, Michael Hobson, Anthony Lasenby,
        nestcheck: diagnostic tests for nested sampling calculations,
        Monthly Notices of the Royal Astronomical Society, Volume 483, Issue 2,
        February 2019, Pages 2044-2056,
        https://doi.org/10.1093/mnras/sty3090

"""
import numpy as np, warnings
from .nsbase import NestedSamplingBase
try:
    import pypolychord
    from pypolychord.settings import PolyChordSettings
except ImportError as err:
    raise err

try:
    import dyPolyChord, dyPolyChord.pypolychord_utils
except ImportError as err:
    raise err

try:
    import nestcheck, nestcheck.data_processing as ncheck_dp, nestcheck.estimators as ncheck_e
except ImportError as err:
    raise err

class dyPolyChordNestedSampling(NestedSamplingBase):
    __doc__ = 'Nested Sampling using dyPolyChord.\n    dyPolyChord: https://github.com/ejhigson/dyPolyChord\n    PolyChord and pypolychord: https://github.com/PolyChord/PolyChordLite\n    Attributes:\n        sampled_parameters (list of :obj:gleipnir.sampled_parameter.SampledParameter):\n            The parameters that are being sampled during the Nested Sampling\n            run.\n        loglikelihood (function): The log-likelihood function to use for\n            assigning a likelihood to parameter vectors during the sampling.\n        population_size (int): The number of points to use in the Nested\n            Sampling active population.\n    References:\n        dyPolyChord\n        1. Higson, (2018). dyPolyChord: dynamic nested sampling with PolyChord.\n            Journal of Open Source Software, 3(29), 965,\n            https://doi.org/10.21105/joss.00965\n        2. Higson, E., Handley, W., Hobson, M. et al. Dynamic nested sampling: an\n            improved algorithm for parameter estimation and evidence calculation.\n            Stat Comput (2018).\n            https://doi.org/10.1007/s11222-018-9844-0\n        PolyChord\n        3. Handley, W. J., M. P. Hobson, and A. N. Lasenby. "PolyChord: nested\n            sampling for cosmology." Monthly Notices of the Royal Astronomical\n            Society: Letters 450.1 (2015): L61-L65.\n        4. Handley, W. J., M. P. Hobson, and A. N. Lasenby. "POLYCHORD:\n            next-generation nested sampling." Monthly Notices of the Royal\n            Astronomical Society 453.4 (2015): 4384-4398.\n        nestcheck\n        5. Edward Higson, Will Handley, Michael Hobson, Anthony Lasenby,\n            nestcheck: diagnostic tests for nested sampling calculations,\n            Monthly Notices of the Royal Astronomical Society, Volume 483, Issue 2,\n            February 2019, Pages 2044-2056,\n            https://doi.org/10.1093/mnras/sty3090\n    '

    def __init__(self, sampled_parameters, loglikelihood, population_size, initial_population_size=None, dynamic_goal=0.5):
        """Initialize the PolyChord Nested Sampler."""
        self.sampled_parameters = sampled_parameters
        self.loglikelihood = loglikelihood
        self.population_size = population_size
        if initial_population_size is None:
            self.initial_population_size = int(population_size / 2)
        else:
            self.initial_population_size = initial_population_size
        self.dynamic_goal = dynamic_goal
        self._nDims = len(sampled_parameters)
        self._nDerived = 0
        self._post_eval = False
        self._posteriors = None

        def likelihood(theta):
            r2 = 0
            return (loglikelihood(theta), [r2])

        self._likelihood = likelihood

        def prior(hypercube):
            return np.array([self.sampled_parameters[i].invcdf(value) for i, value in enumerate(hypercube)])

        self._prior = prior
        self._settings_dict = {'file_root':'dypolychord_run', 
         'base_dir':'dypolychord_chains', 
         'do_clustering':True, 
         'seed':1, 
         'read_resume':False}

    def run(self, verbose=False):
        """Initiate the dyPolyChord Nested Sampling run."""
        dypc_callable = dyPolyChord.pypolychord_utils.RunPyPolyChord(self._likelihood, self._prior, self._nDims)
        dyPolyChord.run_dypolychord(dypc_callable, (self.dynamic_goal), (self._settings_dict),
          ninit=(self.initial_population_size),
          nlive_const=(self.population_size))
        run = nestcheck.data_processing.process_polychord_run(self._settings_dict['file_root'], self._settings_dict['base_dir'])
        self._run = run
        self._logZ = ncheck_e.logz(run)
        self._Z = ncheck_e.evidence(run)
        return (self._logZ, None)

    @property
    def evidence(self):
        """float: Estimate of the Bayesian evidence, or Z."""
        return self._Z

    @evidence.setter
    def evidence(self, value):
        warnings.warn('evidence is not settable')

    @property
    def evidence_error(self):
        """float: Not returned by dyPolyChord->Estimate (rough) of the error in the evidence, or Z.
        The dyPolyChord error could be estimated from multiple runs using a
        bootstrap method provided by nestcheck, but Gleipnir currently doesn't
        bridge this functionality.
        """
        pass

    @evidence_error.setter
    def evidence_error(self, value):
        warnings.warn('evidence_error is not settable')

    @property
    def log_evidence(self):
        """float: Estimate of the natural logarithm of the Bayesian evidence, or ln(Z).
        """
        return self._logZ

    @log_evidence.setter
    def log_evidence(self, value):
        warnings.warn('log_evidence is not settable')

    @property
    def log_evidence_error(self):
        """float: Not returned by dyPolyChord->Estimate of the error in the natural logarithm of the evidence.
        The dyPolyChord error could be estimated from multiple runs using a
        bootstrap method provided by nestcheck, but Gleipnir currently doesn't
        bridge this functionality.
        """
        pass

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
    def dypolychord_file_root(self):
        """str: The file root used by dyPolychord output files."""
        return self._settings_dict['file_root']

    @dypolychord_file_root.setter
    def dypolychord_file_root(self, value):
        self._settings_dict['file_root'] = value

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
            parms = self._run['theta']
            logpw = nestcheck.ns_run_utils.get_logw(self._run)
            if nbins is None:
                nbins = 2 * int(np.cbrt(len(logpw)))
            self._posteriors = dict()
            for ii, parm in enumerate(parms[0]):
                marginal, edge = np.histogram((parms[:, ii]), weights=logpw, density=True, bins=nbins)
                center = (edge[:-1] + edge[1:]) / 2.0
                self._posteriors[self.sampled_parameters[ii].name] = (marginal, edge, center)

            self._post_eval = True
        return self._posteriors

    def max_loglikelihood(self):
        log_likelihoods = self._run['logl']
        ml = log_likelihoods.max()
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
        params = self._run['theta']
        log_likelihoods = self._run['logl']
        weights = nestcheck.ns_run_utils.get_logw(self._run)
        D_of_theta = -2.0 * log_likelihoods
        D_bar = np.average(D_of_theta, weights=weights)
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
        samples = self._run['theta']
        midx = np.argmax(self._run['logl'])
        ml = samples[midx][:]
        return ml