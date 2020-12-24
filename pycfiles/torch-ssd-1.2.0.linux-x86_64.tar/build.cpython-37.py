# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/solver/build.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 669 bytes
import torch
from .lr_scheduler import WarmupMultiStepLR

def make_optimizer(cfg, model, lr=None):
    lr = cfg.SOLVER.BASE_LR if lr is None else lr
    return torch.optim.SGD((model.parameters()), lr=lr, momentum=(cfg.SOLVER.MOMENTUM), weight_decay=(cfg.SOLVER.WEIGHT_DECAY))


def make_lr_scheduler(cfg, optimizer, milestones=None):
    return WarmupMultiStepLR(optimizer=optimizer, milestones=(cfg.SOLVER.LR_STEPS if milestones is None else milestones),
      gamma=(cfg.SOLVER.GAMMA),
      warmup_factor=(cfg.SOLVER.WARMUP_FACTOR),
      warmup_iters=(cfg.SOLVER.WARMUP_ITERS))