# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/torchani/optim.py
# Compiled at: 2020-04-29 02:37:56
# Size of source mod 2**32: 4972 bytes
"""AdamW implementation"""
import math, torch
from torch.optim.optimizer import Optimizer

class AdamW(Optimizer):
    __doc__ = 'Implements AdamW algorithm.\n\n    It has been proposed in `Decoupled Weight Decay Regularization`_.\n\n    Arguments:\n        params (iterable): iterable of parameters to optimize or dicts defining\n            parameter groups\n        lr (float, optional): learning rate (default: 1e-3)\n        betas (Tuple[float, float], optional): coefficients used for computing\n            running averages of gradient and its square (default: (0.9, 0.999))\n        eps (float, optional): term added to the denominator to improve\n            numerical stability (default: 1e-8)\n        weight_decay (float, optional): weight decay factor (default: 0)\n        amsgrad (boolean, optional): whether to use the AMSGrad variant of this\n            algorithm from the paper `On the Convergence of Adam and Beyond`_\n            (default: False)\n\n    .. _Adam\\: A Method for Stochastic Optimization:\n        https://arxiv.org/abs/1412.6980\n    .. _Decoupled Weight Decay Regularization:\n        https://arxiv.org/abs/1711.05101\n    .. _On the Convergence of Adam and Beyond:\n        https://openreview.net/forum?id=ryQu7f-RZ\n    '

    def __init__(self, params, lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, amsgrad=False):
        if not 0.0 <= lr:
            raise ValueError('Invalid learning rate: {}'.format(lr))
        if not 0.0 <= eps:
            raise ValueError('Invalid epsilon value: {}'.format(eps))
        if not 0.0 <= betas[0] < 1.0:
            raise ValueError('Invalid beta parameter at index 0: {}'.format(betas[0]))
        if not 0.0 <= betas[1] < 1.0:
            raise ValueError('Invalid beta parameter at index 1: {}'.format(betas[1]))
        defaults = dict(lr=lr, betas=betas, eps=eps, weight_decay=weight_decay,
          amsgrad=amsgrad)
        super(AdamW, self).__init__(params, defaults)

    def __setstate__(self, state):
        super(AdamW, self).__setstate__(state)
        for group in self.param_groups:
            group.setdefault('amsgrad', False)

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
                    p.data.mul_(1 - group['weight_decay'])
                    grad = p.grad.data
                    if grad.is_sparse:
                        raise RuntimeError('Adam does not support sparse gradients, please consider SparseAdam instead')
                    else:
                        amsgrad = group['amsgrad']
                        state = self.state[p]
                        if len(state) == 0:
                            state['step'] = 0
                            state['exp_avg'] = torch.zeros_like(p.data)
                            state['exp_avg_sq'] = torch.zeros_like(p.data)
                            if amsgrad:
                                state['max_exp_avg_sq'] = torch.zeros_like(p.data)
                        exp_avg, exp_avg_sq = state['exp_avg'], state['exp_avg_sq']
                        if amsgrad:
                            max_exp_avg_sq = state['max_exp_avg_sq']
                        beta1, beta2 = group['betas']
                        state['step'] += 1
                        bias_correction1 = 1 - beta1 ** state['step']
                        bias_correction2 = 1 - beta2 ** state['step']
                        exp_avg.mul_(beta1).add_(1 - beta1, grad)
                        exp_avg_sq.mul_(beta2).addcmul_(1 - beta2, grad, grad)
                        if amsgrad:
                            torch.max(max_exp_avg_sq, exp_avg_sq, out=max_exp_avg_sq)
                            denom = (max_exp_avg_sq.sqrt() / math.sqrt(bias_correction2)).add_(group['eps'])
                        else:
                            denom = (exp_avg_sq.sqrt() / math.sqrt(bias_correction2)).add_(group['eps'])
                    step_size = group['lr'] / bias_correction1
                    p.data.addcdiv_(-step_size, exp_avg, denom)
            else:
                return loss