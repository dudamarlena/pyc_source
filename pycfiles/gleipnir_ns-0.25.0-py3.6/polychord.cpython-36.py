# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gleipnir/polychord.py
# Compiled at: 2019-07-02 15:48:17
# Size of source mod 2**32: 8816 bytes
"""Implementation on top of PolyChord via its python wrapper pypolychord.

This module defines the class for Nested Sampling using using the PolyChord
(i.e., PolyChordLite) program via its Python wrapper pypolychord. Note that
pypolychord has to be built and installed separately (from gleipnir) before
this module can be used.

PolyChordLite: https://github.com/PolyChord/PolyChordLite

References:
    1. Handley, W. J., M. P. Hobson, and A. N. Lasenby. "PolyChord: nested
        sampling for cosmology." Monthly Notices of the Royal Astronomical
        Society: Letters 450.1 (2015): L61-L65.
    2. Handley, W. J., M. P. Hobson, and A. N. Lasenby. "POLYCHORD:
        next-generation nested sampling." Monthly Notices of the Royal
        Astronomical Society 453.4 (2015): 4384-4398.

"""
import numpy as np, scipy, warnings
from .nsbase import NestedSamplingBase
try:
    import pypolychord
    from pypolychord.settings import PolyChordSettings
except ImportError as err:
    raise err

class PolyChordNestedSampling(NestedSamplingBase):
    __doc__ = 'Nested Sampling using PolyChord.\n    PolyChord and pypolychord: https://github.com/PolyChord/PolyChordLites\n    Attributes:\n        sampled_parameters (list of :obj:gleipnir.sampled_parameter.SampledParameter):\n            The parameters that are being sampled during the Nested Sampling\n            run.\n        loglikelihood (function): The log-likelihood function to use for\n            assigning a likelihood to parameter vectors during the sampling.\n        population_size (int): The number of points to use in the Nested\n            Sampling active population.\n    References:\n        1. Handley, W. J., M. P. Hobson, and A. N. Lasenby. "PolyChord: nested\n            sampling for cosmology." Monthly Notices of the Royal Astronomical\n            Society: Letters 450.1 (2015): L61-L65.\n        2. Handley, W. J., M. P. Hobson, and A. N. Lasenby. "POLYCHORD:\n            next-generation nested sampling." Monthly Notices of the Royal\n            Astronomical Society 453.4 (2015): 4384-4398.\n    '

    def __init__(self, sampled_parameters, loglikelihood, population_size):
        """Initialize the PolyChord Nested Sampler."""
        self.sampled_parameters = sampled_parameters
        self.loglikelihood = loglikelihood
        self.population_size = population_size
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
        self._settings = PolyChordSettings((self._nDims), (self._nDerived), nlive=(self.population_size))
        self._settings.file_root = 'polychord_run'
        self._settings.do_clustering = True
        self._settings.read_resume = False

        def dumper(live, dead, logweights, logZ, logZerr):
            print('Last dead point:', dead[(-1)])

        self._dumper = dumper

    def run(self, verbose=False):
        """Initiate the PolyChord Nested Sampling run."""
        output = pypolychord.run_polychord(self._likelihood, self._nDims, self._nDerived, self._settings, self._prior, self._dumper)
        self._output = output
        return (output.logZ, output.logZerr)

    @property
    def evidence(self):
        """float: Estimate of the Bayesian evidence, or Z."""
        return np.exp(self._output.logZ)

    @evidence.setter
    def evidence(self, value):
        warnings.warn('evidence is not settable')

    @property
    def evidence_error(self):
        """float: Estimate (rough) of the error in the evidence, or Z."""
        return np.exp(self._output.logZerr)

    @evidence_error.setter
    def evidence_error(self, value):
        warnings.warn('evidence_error is not settable')

    @property
    def log_evidence(self):
        """float: Estimate of the natural logarithm of the Bayesian evidence, or ln(Z).
        """
        return self._output.logZ

    @log_evidence.setter
    def log_evidence(self, value):
        warnings.warn('log_evidence is not settable')

    @property
    def log_evidence_error(self):
        """float: Estimate of the error in the natural logarithm of the evidence.
        """
        return self._output.logZerr

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
    def polychord_file_root(self):
        """str: The file root used by Polychord output files."""
        return self._settings.file_root

    @polychord_file_root.setter
    def polychord_file_root(self, value):
        self._settings.file_root = value

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
            samples = self._output.samples
            log_likelihoods = samples['loglike'].to_numpy()
            parms = samples.columns[2:]
            if nbins is None:
                nbins = 2 * int(np.cbrt(len(log_likelihoods)))
            self._posteriors = dict()
            for ii, parm in enumerate(parms):
                marginal, edge = np.histogram((samples[parm]), density=True, bins=nbins)
                center = (edge[:-1] + edge[1:]) / 2.0
                self._posteriors[self.sampled_parameters[ii].name] = (marginal, edge, center)

            self._post_eval = True
        return self._posteriors

    def max_loglikelihood(self):
        samples = self._output.samples
        mx = samples.max()
        ml = mx['loglike']
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
        samples = self._output.samples
        log_likelihoods = samples['loglike'].to_numpy()
        parms = samples.columns[2:]
        params = samples[parms]
        D_of_theta = -2.0 * log_likelihoods
        D_bar = np.average(D_of_theta)
        theta_bar = np.average(params, axis=0)
        print(theta_bar)
        D_of_theta_bar = -2.0 * self.loglikelihood(theta_bar)
        p_D = D_bar - D_of_theta_bar
        return p_D + D_bar

    def best_fit_likelihood(self):
        """Parameter vector with the maximum likelihood.
        Returns:
            numpy.array: The parameter vector.
        """
        samples = self._output.samples
        midx = np.argmax(samples['loglike'].values)
        ml = samples.values[midx][2:]
        return ml