# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/data/samplers/iteration_based_batch_sampler.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 1093 bytes
from torch.utils.data.sampler import BatchSampler

class IterationBasedBatchSampler(BatchSampler):
    __doc__ = '\n    Wraps a BatchSampler, re-sampling from it until\n    a specified number of iterations have been sampled\n    '

    def __init__(self, batch_sampler, num_iterations, start_iter=0):
        self.batch_sampler = batch_sampler
        self.num_iterations = num_iterations
        self.start_iter = start_iter

    def __iter__(self):
        iteration = self.start_iter
        while iteration <= self.num_iterations:
            if hasattr(self.batch_sampler.sampler, 'set_epoch'):
                self.batch_sampler.sampler.set_epoch(iteration)
            for batch in self.batch_sampler:
                iteration += 1
                if iteration > self.num_iterations:
                    break
                yield batch

    def __len__(self):
        return self.num_iterations