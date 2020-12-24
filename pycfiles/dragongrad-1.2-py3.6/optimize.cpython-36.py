# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/autograd/optimize.py
# Compiled at: 2018-12-11 19:53:54
# Size of source mod 2**32: 3294 bytes
import numpy as np

class Optimizer:
    __doc__ = '\n    Optimizer Base Class\n\n    == Args ==\n\n    loss_func (function): a function accepting a list of `params` (see below) and returning a tuple (data, gradient)\n    params (array): a list of initialization parameters - these should correspond to the parameters of the loss_func\n    lr (float): leaning rate for steps\n    tol (float): tolerance for determining loss function convergence\n    max_iter (int): maximumer number of steps the optimizer will run\n\n    '

    def __init__(self, loss_func, params, lr=0.01, max_iter=100000, tol=1e-14):
        self.loss_func = loss_func
        self.params = params
        self.lr = lr
        self.max_iter = max_iter
        self.tol = tol

    def step(self):
        """
        Performs a single step of the optimizaiton
        """
        raise NotImplementedError

    def solve(self, return_steps=False):
        """
        Loop until convergence criteria is met or for max_iters
        """
        steps = []
        count = 0
        while count < self.max_iter:
            prev_loss, prev_grad = self.loss_func(self.params)
            self.step()
            new_loss, new_grad = self.loss_func(self.params)
            if return_steps:
                steps.append(self.params)
            if abs(prev_loss - new_loss) < self.tol:
                break
            count += 1

        if return_steps:
            return (self.params, steps)
        else:
            return self.params


class GD(Optimizer):
    __doc__ = '\n    Gradient Descent Optimizer\n    '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)

    def step(self):
        loss, grad = self.loss_func(self.params)
        grad = grad[0]
        self.params = self.params - self.lr * grad


class Adam(Optimizer):
    __doc__ = '\n    Implements Adam Optimizer (`Adam: A Method for Stochastic Optimization`)\n    '

    def __init__(self, *args, beta1=0.9, beta2=0.999, eps=1e-08, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.exp_avg = np.zeros_like(self.params)
        self.exp_avg_sq = np.zeros_like(self.params)
        self.step_count = 0

    def step(self):
        self.step_count += 1
        loss, grad = self.loss_func(self.params)
        grad = grad[0]
        self.exp_avg = self.exp_avg * self.beta1 + (1 - self.beta1) * grad
        self.exp_avg_sq = self.exp_avg_sq * self.beta2 + (1 - self.beta2) * grad ** 2
        bias_correction1 = self.exp_avg / (1 - self.beta1 ** self.step_count)
        bias_correction2 = self.exp_avg_sq / (1 - self.beta2 ** self.step_count)
        step_size = self.lr * bias_correction1 / (np.sqrt(bias_correction2) + self.eps)
        self.params = self.params - step_size