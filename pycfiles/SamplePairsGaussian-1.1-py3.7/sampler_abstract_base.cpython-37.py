# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/samplePairsGaussian/sampler_abstract_base.py
# Compiled at: 2019-06-29 01:01:29
# Size of source mod 2**32: 3325 bytes
from abc import ABC, abstractmethod
import numpy as np, logging

class SamplerAbstractBase(ABC):
    __doc__ = 'Sampler class.\n\n    Attributes:\n    prob_calculator (ProbCalculator): probability calculator\n    idx_chosen (int): the idx chosen\n\n    Private attributes:\n    _logger (logger): logging\n    '

    def __init__(self, prob_calculator):
        """Constructor. Also computes distances.

        Args:
        prob_calculator (ProbCalculator): probability calculator
        """
        self._logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        self._logger.setLevel(logging.ERROR)
        self.prob_calculator = prob_calculator
        self.idx_chosen = None

    def set_logging_level(self, level):
        """Sets the logging level

        Args:
        level (logging): logging level
        """
        self._logger.setLevel(level)

    @abstractmethod
    def rejection_sample(self, no_tries_max=100):
        """Use rejection sampling to sample the pair

        Args:
        no_tries_max (int): max. no. of tries for rejection sampling

        Returns:
        bool: True for success, False for failure
        """
        if self.prob_calculator.no_idx_pairs_possible == 0:
            self._logger.info('> samplePairsGaussian < [base] Fail: not enough pairs within the cutoff radius to sample a pair.')
            return False
        self.idx_chosen = None
        i_try = 0
        while i_try < no_tries_max:
            i_try += 1
            idx_pair = np.random.randint(self.prob_calculator.no_idx_pairs_possible)
            r = np.random.uniform(0.0, self.prob_calculator.max_prob)
            if r < self.prob_calculator.probs[idx_pair]:
                self.idx_chosen = idx_pair
                self._logger.info('> samplePairsGaussian < [base] Accepted idx: ' + str(self.idx_chosen) + ' after: ' + str(i_try) + ' tries')
                return True

        self._logger.info('> samplePairsGaussian < [base] Fail: Could not rejection sample the pair after: ' + str(i_try) + ' tries.')
        return False

    @abstractmethod
    def cdf_sample(self):
        """Sample by directly calculating the CDF via np.random.choice

        Returns:
        bool: True for success, False for failure
        """
        if self.prob_calculator.no_idx_pairs_possible == 0:
            self._logger.info('> samplePairsGaussian < [base] Fail: not enough pairs within the cutoff radius to sample a pair.')
            return False
        self.idx_chosen = np.random.choice((range(self.prob_calculator.no_idx_pairs_possible)), 1, p=(self.prob_calculator.probs))[0]
        self._logger.info('> samplePairsGaussian < [base] CDF sampled idx: ' + str(self.idx_chosen))
        return True