# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/data/samplers/distributed.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 2568 bytes
import math, torch
import torch.distributed as dist
from torch.utils.data.sampler import Sampler

class DistributedSampler(Sampler):
    __doc__ = 'Sampler that restricts data loading to a subset of the dataset.\n    It is especially useful in conjunction with\n    :class:`torch.nn.parallel.DistributedDataParallel`. In such case, each\n    process can pass a DistributedSampler instance as a DataLoader sampler,\n    and load a subset of the original dataset that is exclusive to it.\n    .. note::\n        Dataset is assumed to be of constant size.\n    Arguments:\n        dataset: Dataset used for sampling.\n        num_replicas (optional): Number of processes participating in\n            distributed training.\n        rank (optional): Rank of the current process within num_replicas.\n    '

    def __init__(self, dataset, num_replicas=None, rank=None, shuffle=True):
        if num_replicas is None:
            if not dist.is_available():
                raise RuntimeError('Requires distributed package to be available')
            num_replicas = dist.get_world_size()
        if rank is None:
            if not dist.is_available():
                raise RuntimeError('Requires distributed package to be available')
            rank = dist.get_rank()
        self.dataset = dataset
        self.num_replicas = num_replicas
        self.rank = rank
        self.epoch = 0
        self.num_samples = int(math.ceil(len(self.dataset) * 1.0 / self.num_replicas))
        self.total_size = self.num_samples * self.num_replicas
        self.shuffle = shuffle

    def __iter__(self):
        if self.shuffle:
            g = torch.Generator()
            g.manual_seed(self.epoch)
            indices = torch.randperm((len(self.dataset)), generator=g).tolist()
        else:
            indices = torch.arange(len(self.dataset)).tolist()
        indices += indices[:self.total_size - len(indices)]
        assert len(indices) == self.total_size
        offset = self.num_samples * self.rank
        indices = indices[offset:offset + self.num_samples]
        assert len(indices) == self.num_samples
        return iter(indices)

    def __len__(self):
        return self.num_samples

    def set_epoch(self, epoch):
        self.epoch = epoch