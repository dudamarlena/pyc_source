# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/samplePairsGaussian/sampler.py
# Compiled at: 2019-06-29 17:29:53
# Size of source mod 2**32: 2337 bytes
from .sampler_abstract_base import *
from .prob_calculator import *
import numpy as np

class Sampler(SamplerAbstractBase):
    __doc__ = 'Sampler class.\n\n    Attributes:\n    idx_first_particle (int): idx of the first particle chosen\n    idx_second_particle (int): idx of the second particle chosen\n    '

    def __init__(self, prob_calculator):
        super().__init__(prob_calculator)
        self.idx_first_particle = None
        self.idx_second_particle = None

    def rejection_sample(self, no_tries_max=100):
        """Use rejection sampling to sample the pair

        Args:
        no_tries_max (int): max. no. of tries for rejection sampling

        Returns:
        bool: True for success, False for failure
        """
        self.idx_first_particle = None
        self.idx_second_particle = None
        success = super().rejection_sample(no_tries_max=no_tries_max)
        if success:
            self.idx_first_particle = self.prob_calculator.probs_idxs_first_particle[self.idx_chosen]
            self.idx_second_particle = self.prob_calculator.probs_idxs_second_particle[self.idx_chosen]
            self._logger.info('> samplePairsGaussian < Accepted pair idxs: ' + str(self.idx_first_particle) + ' ' + str(self.idx_second_particle))
            return True
        return False

    def cdf_sample(self):
        self.idx_first_particle = None
        self.idx_second_particle = None
        success = super().cdf_sample()
        if success:
            self.idx_first_particle = self.prob_calculator.probs_idxs_first_particle[self.idx_chosen]
            self.idx_second_particle = self.prob_calculator.probs_idxs_second_particle[self.idx_chosen]
            self._logger.info('> samplePairsGaussian < Accepted pair idxs: ' + str(self.idx_first_particle) + ' ' + str(self.idx_second_particle))
            return True
        return False