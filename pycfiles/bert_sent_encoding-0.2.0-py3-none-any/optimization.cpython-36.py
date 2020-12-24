# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/sjzwind/5829E2A27A97CAA9/PycharmProjects/bert-sent-encoding/bert_sent_encoding/pytorch_pretrained_bert/optimization.py
# Compiled at: 2019-01-22 06:01:06
# Size of source mod 2**32: 6802 bytes
"""PyTorch optimization for BERT model."""
import math, torch
from torch.optim import Optimizer
from torch.optim.optimizer import required
from torch.nn.utils import clip_grad_norm_

def warmup_cosine(x, warmup=0.002):
    if x < warmup:
        return x / warmup
    else:
        return 0.5 * (1.0 + torch.cos(math.pi * x))


def warmup_constant(x, warmup=0.002):
    if x < warmup:
        return x / warmup
    else:
        return 1.0


def warmup_linear(x, warmup=0.002):
    if x < warmup:
        return x / warmup
    else:
        return 1.0 - x


SCHEDULES = {'warmup_cosine':warmup_cosine, 
 'warmup_constant':warmup_constant, 
 'warmup_linear':warmup_linear}

class BertAdam(Optimizer):
    __doc__ = "Implements BERT version of Adam algorithm with weight decay fix.\n    Params:\n        lr: learning rate\n        warmup: portion of t_total for the warmup, -1  means no warmup. Default: -1\n        t_total: total number of training steps for the learning\n            rate schedule, -1  means constant learning rate. Default: -1\n        schedule: schedule to use for the warmup (see above). Default: 'warmup_linear'\n        b1: Adams b1. Default: 0.9\n        b2: Adams b2. Default: 0.999\n        e: Adams epsilon. Default: 1e-6\n        weight_decay: Weight decay. Default: 0.01\n        max_grad_norm: Maximum norm for the gradients (-1 means no clipping). Default: 1.0\n    "

    def __init__(self, params, lr=required, warmup=-1, t_total=-1, schedule='warmup_linear', b1=0.9, b2=0.999, e=1e-06, weight_decay=0.01, max_grad_norm=1.0):
        if lr is not required:
            if lr < 0.0:
                raise ValueError('Invalid learning rate: {} - should be >= 0.0'.format(lr))
            else:
                if schedule not in SCHEDULES:
                    raise ValueError('Invalid schedule parameter: {}'.format(schedule))
                if not 0.0 <= warmup < 1.0:
                    if not warmup == -1:
                        raise ValueError('Invalid warmup: {} - should be in [0.0, 1.0[ or -1'.format(warmup))
            if not 0.0 <= b1 < 1.0:
                raise ValueError('Invalid b1 parameter: {} - should be in [0.0, 1.0['.format(b1))
        else:
            if not 0.0 <= b2 < 1.0:
                raise ValueError('Invalid b2 parameter: {} - should be in [0.0, 1.0['.format(b2))
            raise e >= 0.0 or ValueError('Invalid epsilon value: {} - should be >= 0.0'.format(e))
        defaults = dict(lr=lr, schedule=schedule, warmup=warmup, t_total=t_total, b1=b1,
          b2=b2,
          e=e,
          weight_decay=weight_decay,
          max_grad_norm=max_grad_norm)
        super(BertAdam, self).__init__(params, defaults)

    def get_lr(self):
        lr = []
        for group in self.param_groups:
            for p in group['params']:
                state = self.state[p]
                if len(state) == 0:
                    return [
                     0]
                if group['t_total'] != -1:
                    schedule_fct = SCHEDULES[group['schedule']]
                    lr_scheduled = group['lr'] * schedule_fct(state['step'] / group['t_total'], group['warmup'])
                else:
                    lr_scheduled = group['lr']
                lr.append(lr_scheduled)

        return lr

    def step(self, closure=None):
        """Performs a single optimization step.
        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    pass
                else:
                    grad = p.grad.data
                    if grad.is_sparse:
                        raise RuntimeError('Adam does not support sparse gradients, please consider SparseAdam instead')
                    state = self.state[p]
                    if len(state) == 0:
                        state['step'] = 0
                        state['next_m'] = torch.zeros_like(p.data)
                        state['next_v'] = torch.zeros_like(p.data)
                    next_m, next_v = state['next_m'], state['next_v']
                    beta1, beta2 = group['b1'], group['b2']
                    if group['max_grad_norm'] > 0:
                        clip_grad_norm_(p, group['max_grad_norm'])
                    next_m.mul_(beta1).add_(1 - beta1, grad)
                    next_v.mul_(beta2).addcmul_(1 - beta2, grad, grad)
                    update = next_m / (next_v.sqrt() + group['e'])
                    if group['weight_decay'] > 0.0:
                        update += group['weight_decay'] * p.data
                    if group['t_total'] != -1:
                        schedule_fct = SCHEDULES[group['schedule']]
                        lr_scheduled = group['lr'] * schedule_fct(state['step'] / group['t_total'], group['warmup'])
                    else:
                        lr_scheduled = group['lr']
                    update_with_lr = lr_scheduled * update
                    p.data.add_(-update_with_lr)
                    state['step'] += 1

        return loss