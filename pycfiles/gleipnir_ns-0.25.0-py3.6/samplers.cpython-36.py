# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gleipnir/samplers.py
# Compiled at: 2019-03-13 19:52:46
# Size of source mod 2**32: 7181 bytes
"""Samplers used to update points from Nested Sampling.

This module defines the classes for the samplers used to update a chosen
survivor point in order to replace the dead point during the
Nested Sampling runs via the gleipnir.nested_sampling.NestedSampling class.

"""
import numpy as np
from scipy.stats import uniform, norm

class MetropolisComponentWiseHardNSRejection(object):
    __doc__ = 'Markov Chain Monte Carlo sampler using augmented Metropolis criterion and component-wise trial moves.\n    This sampler uses a Markov Chain Monte Carlo method to augment a position\n    as sampled from the prior density using the Metropolis criterion and an extra\n    hard rejection for the Nested Sampling likelihood level. Trial moves\n    are carried out in a component-wise fashion (i.e., parameters are looped over\n    in order).\n\n    Attributes:\n        iterations (int): The number of component-wise trial move cycles. The\n            total number of trial moves will be iterations*ndim. Default: 100\n        burn_in (int): The number of additional burn in iterations to\n            to run in order to "equilibrate" the Markov chain. Default: 0\n        tuning_cycles (int): The number of tuning cycles to run before the\n            Markov chain in order to tune the step sizes of the trial moves.\n            Each tuning cycle is 20 iterations, after which the trial move step\n            sizes are updated to try and make the acceptance ratio between\n            0.2 and 0.6. Default: 0\n        proposal (str): The shape of the symmetric proposal distrbution to\n            use during the trial moves. The proposal can either be "uniform"\n            or "normal." Default: "uniform"\n    References:\n        None\n    '

    def __init__(self, iterations=100, burn_in=0, tuning_cycles=0, proposal='uniform'):
        """Initialize the sampler."""
        self.iterations = iterations
        self.burn_in = burn_in
        self.tuning_cycles = tuning_cycles
        self.proposal = proposal
        self._first = True
        self._widths = list()
        self._ndim = None

    def __call__(self, sampled_parameters, loglikelihood, start_param_vec, ns_boundary, **kwargs):
        """Run the sampler.

        Args:
            sampled_parameters (:obj:`list` of
                :obj:`gleipnir.sampled_parameter.SampledParameter`): The
                parameters that are being sampled.
            loglikelihood (function): The log likelihood function.
            start_param_vec (obj:`numpy.ndarray`): The starting position of
                parameter vector for the parameters being sampled.
            ns_boundary (float): The current lower likelihood bound from the
            Nested Sampling routine.
            kwargs (dict): Pass in any other method specific keyword arguments.
        """
        if self._first:
            self._ndim = len(sampled_parameters)
            for sampled_parameter in sampled_parameters:
                rs = sampled_parameter.rvs(100)
                mirs = np.min(rs)
                mars = np.max(rs)
                width = mars - mirs
                self._widths.append(0.5 * width)

            self._widths = np.array(self._widths)
            self._first = False
        start_likelihood = loglikelihood(start_param_vec)
        steps = self._widths.copy()
        acceptance = np.zeros(self._ndim)
        cur_point = start_param_vec.copy()
        cur_likelihood = start_likelihood
        for i in range(self.tuning_cycles):
            for k in range(20):
                rsteps = np.random.random(self._ndim)
                u = np.random.random(self._ndim)
                for j in range(self._ndim):
                    new_point = cur_point.copy()
                    cur_pointj = cur_point[j]
                    widthj = self._widths[j]
                    if self.proposal == 'normal':
                        new_pointj = norm.ppf((rsteps[j]), loc=cur_pointj, scale=widthj)
                    else:
                        new_pointj = uniform.ppf((rsteps[j]), loc=(cur_pointj - widthj / 2.0), scale=widthj)
                    new_point[j] = new_pointj
                    cur_priorj = sampled_parameters[j].prior(cur_pointj)
                    new_priorj = sampled_parameters[j].prior(new_point[j])
                    ratio = new_priorj / cur_priorj
                    new_likelihood = loglikelihood(new_point)
                    if u[j] < ratio and new_likelihood > ns_boundary:
                        cur_point[j] = new_pointj
                        cur_likelihood = new_likelihood
                        acceptance[j] += 1.0

                acceptance_ratio = acceptance / 20.0
                less_than_mask = acceptance_ratio < 0.2
                gt_mask = acceptance_ratio > 0.6
                steps[less_than_mask] *= 0.66
                steps[gt_mask] *= 1.33
                acceptance[:] = 0.0

        self._widths = steps.copy()
        cur_point = start_param_vec.copy()
        curr_likelihood = start_likelihood
        for i in range(self.iterations + self.burn_in):
            rsteps = np.random.random(self._ndim)
            u = np.random.random(self._ndim)
            for j in range(self._ndim):
                new_point = cur_point.copy()
                cur_pointj = cur_point[j]
                widthj = self._widths[j]
                if self.proposal == 'normal':
                    new_pointj = norm.ppf((rsteps[j]), loc=cur_pointj, scale=widthj)
                else:
                    new_pointj = uniform.ppf((rsteps[j]), loc=(cur_pointj - widthj / 2.0), scale=widthj)
                cur_priorj = sampled_parameters[j].prior(cur_pointj)
                new_priorj = sampled_parameters[j].prior(new_point[j])
                ratio = new_priorj / cur_priorj
                new_likelihood = loglikelihood(new_point)
                if u[j] < ratio and new_likelihood > ns_boundary:
                    cur_point[j] = new_pointj
                    cur_likelihood = new_likelihood

        return (
         cur_point, cur_likelihood)