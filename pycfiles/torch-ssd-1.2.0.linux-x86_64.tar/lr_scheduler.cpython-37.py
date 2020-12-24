# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/solver/lr_scheduler.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 1080 bytes
from bisect import bisect_right
from torch.optim.lr_scheduler import _LRScheduler

class WarmupMultiStepLR(_LRScheduler):

    def __init__(self, optimizer, milestones, gamma=0.1, warmup_factor=0.3333333333333333, warmup_iters=500, last_epoch=-1):
        if not list(milestones) == sorted(milestones):
            raise ValueError('Milestones should be a list of increasing integers. Got {}', milestones)
        self.milestones = milestones
        self.gamma = gamma
        self.warmup_factor = warmup_factor
        self.warmup_iters = warmup_iters
        super().__init__(optimizer, last_epoch)

    def get_lr(self):
        warmup_factor = 1
        if self.last_epoch < self.warmup_iters:
            alpha = float(self.last_epoch) / self.warmup_iters
            warmup_factor = self.warmup_factor * (1 - alpha) + alpha
        return [base_lr * warmup_factor * self.gamma ** bisect_right(self.milestones, self.last_epoch) for base_lr in self.base_lrs]