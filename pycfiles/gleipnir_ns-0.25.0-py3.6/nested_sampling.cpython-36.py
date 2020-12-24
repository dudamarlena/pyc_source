# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gleipnir/nested_sampling.py
# Compiled at: 2019-03-14 18:41:15
# Size of source mod 2**32: 12825 bytes
"""Implementation of Nested Sampling.

This module defines the class used for Nested Sampling.

References:
    1. Skilling, John. "Nested sampling." AIP Conference Proceedings. Vol.
        735. No. 1. AIP, 2004.
    2. Skilling, John. "Nested sampling for general Bayesian computation."
        Bayesian analysis 1.4 (2006): 833-859.
    3. Skilling, John. "Nested sampling’s convergence." AIP Conference
        Proceedings. Vol. 1193. No. 1. AIP, 2009.
"""
import numpy as np, pandas as pd, warnings

class NestedSampling(object):
    __doc__ = 'A Nested Sampler.\n    This class is an implementation of the outer layer of the classic Nested\n    Sampling algorithm.\n\n    Attributes:\n        sampled_parameters (list of :obj:gleipnir.sampled_parameter.SampledParameter):\n            The parameters that are being sampled during the Nested Sampling\n            run.\n        loglikelihood (function): The log-likelihood function to use for\n            assigning a likelihood to parameter vectors during the sampling.\n        sampler (obj from gleipnir.samplers): The sampling scheme to be used\n            when updating sample points.\n        population_size (int): The number of points to use in the Nested\n            Sampling active population.\n        stopping_criterion (obj from gleipnir.stopping_criterion): The criterion\n            that should be used to determine when to stop the Nested Sampling\n            run.\n    References:\n        1. Skilling, John. "Nested sampling." AIP Conference Proceedings. Vol.\n            735. No. 1. AIP, 2004.\n        2. Skilling, John. "Nested sampling for general Bayesian computation."\n            Bayesian analysis 1.4 (2006): 833-859.\n        3. Skilling, John. "Nested sampling’s convergence." AIP Conference\n            Proceedings. Vol. 1193. No. 1. AIP, 2009.\n    '

    def __init__(self, sampled_parameters, loglikelihood, sampler, population_size, stopping_criterion):
        """Initialize the Nested Sampler."""
        self.sampled_parameters = sampled_parameters
        self._sampled_parameters_dict = {sp.name:sp for sp in sampled_parameters}
        self.loglikelihood = loglikelihood
        self.sampler = sampler
        self.population_size = population_size
        self.stopping_criterion = stopping_criterion
        self._alpha = population_size / (population_size + 1)
        self._evidence = 0.0
        self._evidence_error = 0.0
        self._logZ_err = 0.0
        self._log_evidence = 0.0
        self._information = 0.0
        self._H = 0.0
        self._previous_evidence = 0.0
        self._current_weights = 1.0
        self._previous_weight = 1.0
        self._n_iterations = 0
        self._dead_points = list()
        self._live_points = None
        self._post_eval = False
        self._posteriors = None

    def run(self, verbose=False):
        """Initiate the Nested Sampling run.
        Returns:
            tuple of (float, float): Tuple containing the natural logarithm
            of the evidence and its error estimate as computed from the
            Nested Sampling run: (log_evidence, log_evidence_error)
        """
        if verbose:
            print('Generating the initial set of live points with population size {}...'.format(self.population_size))
        else:
            live_points = dict()
            for i in range(self.population_size):
                for sampled_parameter_name in self._sampled_parameters_dict:
                    name = sampled_parameter_name
                    rs = self._sampled_parameters_dict[sampled_parameter_name].rvs(1)[0]
                    if name not in live_points.keys():
                        live_points[name] = list([rs])
                    else:
                        live_points[name].append(rs)

            self._live_points = pd.DataFrame(live_points)
            if verbose:
                print('Evaluating the loglikelihood function for each live point...')
            log_likelihoods = np.array([self.loglikelihood(sampled_parameter_vector) for sampled_parameter_vector in self._live_points.values])
            self._n_iterations += 1
            self._current_weights = 1.0 - self._alpha ** self._n_iterations
            ndx = np.argmin(log_likelihoods)
            log_l = log_likelihoods[ndx]
            param_vec = self._live_points.values[ndx]
            dZ = self._current_weights * np.exp(log_l)
            self._evidence += dZ
            dH = dZ * log_l
            if np.isnan(dH):
                dH = 0.0
            self._H += dH
            if self._evidence > 0.0:
                self._information = -np.log(self._evidence) + self._H / self._evidence
            self._previous_weight = self._current_weights
            dpd = dict({'log_l':log_l,  'weight':self._current_weights})
            for k, val in enumerate(param_vec):
                dpd[self.sampled_parameters[k].name] = val

            self._dead_points.append(dpd)
            if verbose:
                print('Iteration: {} Evidence estimate: {} Remaining prior mass: {}'.format(self._n_iterations, self._evidence, self._alpha ** self._n_iterations))
                print('Dead Point:')
                print(self._dead_points[(-1)])
            while not self._stopping_criterion():
                self._n_iterations += 1
                self._current_weights = self._alpha ** (self._n_iterations - 1.0) - self._alpha ** self._n_iterations
                r_p_ndx = int(np.random.random(1) * self.population_size)
                while r_p_ndx == ndx:
                    r_p_ndx = int(np.random.random(1) * self.population_size)

                r_p_param_vec = self._live_points.values[r_p_ndx]
                updated_point_param_vec, u_log_l = self.sampler(self.sampled_parameters, self.loglikelihood, r_p_param_vec, log_l)
                log_likelihoods[ndx] = u_log_l
                self._live_points.values[ndx] = updated_point_param_vec
                ndx = np.argmin(log_likelihoods)
                log_l = log_likelihoods[ndx]
                param_vec = self._live_points.values[ndx]
                dZ = self._current_weights * np.exp(log_l)
                self._evidence += dZ
                dH = dZ * log_l
                if np.isnan(dH):
                    dH = 0.0
                self._H += dH
                if self._evidence > 0.0:
                    self._information = -np.log(self._evidence) + self._H / self._evidence
                dpd = dict({'log_l':log_l,  'weight':self._current_weights})
                for k, val in enumerate(param_vec):
                    dpd[self.sampled_parameters[k].name] = val

                self._dead_points.append(dpd)
                self._previous_weight = self._current_weights
                if verbose and self._n_iterations % 10 == 0:
                    logZ_err = np.sqrt(self._information / self.population_size)
                    ev_err = np.exp(logZ_err)
                    print('Iteration: {} Evidence estimate: {} +- {} Remaining prior mass: {}'.format(self._n_iterations, self._evidence, ev_err, self._alpha ** self._n_iterations))
                    print('Dead Point:')
                    print(self._dead_points[(-1)])

            weight = self._alpha ** self._n_iterations
            likelihoods = np.exp(log_likelihoods)
            likelihoods_surv = np.array([likelihood for i, likelihood in enumerate(likelihoods) if i != ndx])
            l_m = likelihoods_surv.mean()
            self._evidence += weight * l_m
            dH = weight * l_m * np.log(l_m)
            if np.isnan(dH):
                dH = 0.0
            self._H += dH
            if self._evidence > 0.0:
                self._information = -np.log(self._evidence) + self._H / self._evidence
        n_left = len(likelihoods_surv)
        a_weight = weight / n_left
        for i, l_likelihood in enumerate(log_likelihoods):
            if i != ndx:
                dpd = dict({'log_l':l_likelihood,  'weight':a_weight})
                for k, val in enumerate(self._live_points.values[i]):
                    dpd[self.sampled_parameters[k].name] = val

                self._dead_points.append(dpd)

        logZ_err = np.sqrt(self._information / self.population_size)
        self._logZ_err = logZ_err
        ev_err = np.exp(logZ_err)
        self._evidence_error = ev_err
        self._log_evidence = np.log(self._evidence)
        self._dead_points = pd.DataFrame(self._dead_points)
        return (
         self._log_evidence, logZ_err)

    def _stopping_criterion(self):
        """Wrapper function for the stopping criterion."""
        return self.stopping_criterion(self)

    @property
    def evidence(self):
        """float: Estimate of the Bayesian evidence, or Z.
        """
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
        """float: Estimate (rough) of the error in the natural logarithm of the evidence.
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

    def posteriors(self):
        """Estimates of the posterior marginal probability distributions of each parameter.
        Returns:
            dict of tuple of (numpy.ndarray, numpy.ndarray): The histogram
                estimates of the posterior marginal probability distributions.
                The returned dict is keyed by the sampled parameter names and
                each element is a tuple with (marginal_weights, bin_centers).
        """
        if not self._post_eval:
            log_likelihoods = self._dead_points['log_l'].to_numpy()
            weights = self._dead_points['weight'].to_numpy()
            likelihoods = np.exp(log_likelihoods)
            norm_weights = weights * likelihoods / self.evidence
            gt_mask = norm_weights > 0.0
            parms = self._dead_points.columns[2:]
            nbins = 2 * int(np.cbrt(len(norm_weights[gt_mask])))
            self._posteriors = dict()
            for parm in parms:
                marginal, edge = np.histogram((self._dead_points[parm][gt_mask]), weights=(norm_weights[gt_mask]), density=True, bins=nbins)
                center = (edge[:-1] + edge[1:]) / 2.0
                self._posteriors[parm] = (marginal, center)

            self._post_eval = True
        return self._posteriors

    @property
    def dead_points(self):
        """The set of dead points collected during the Nested Sampling run."""
        return self._dead_points

    @dead_points.setter
    def dead_points(self, value):
        warnings.warn('dead_points is not settable')