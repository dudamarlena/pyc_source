# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./ulangel/utils/callbacks.py
# Compiled at: 2020-03-05 08:23:54
# Size of source mod 2**32: 6314 bytes
import math, re
from functools import partial
from typing import Iterable
import matplotlib.pyplot as plt
import torch
_camel_re1 = re.compile('(.)([A-Z][a-z]+)')
_camel_re2 = re.compile('([a-z0-9])([A-Z])')

def camel2snake(name):
    """standardize the callback name into a camel2snake format"""
    s1 = re.sub(_camel_re1, '\\1_\\2', name)
    return re.sub(_camel_re2, '\\1_\\2', s1).lower()


def listify(o):
    """Turn all non-list-type object into a list"""
    if o is None:
        return []
    if isinstance(o, list):
        return o
    if isinstance(o, str):
        return [
         o]
    if isinstance(o, Iterable):
        return list(o)
    return [
     o]


class CancelTrainException(Exception):
    pass


class CancelEpochException(Exception):
    pass


class CancelBatchException(Exception):
    pass


class Callback:
    __doc__ = 'Callback class as a trigger to do some special calculation during the\n    training.\n    '
    _order = 0

    def set_runner(self, run):
        self.run = run

    def __getattr__(self, k):
        return getattr(self.run, k)

    @property
    def name(self):
        name = re.sub('Callback$', '', self.__class__.__name__)
        return camel2snake(name or 'callback')

    def __call__(self, cb_name):
        f = getattr(self, cb_name, None)
        if f:
            if f():
                return True
        return False


class TrainEvalCallback(Callback):
    __doc__ = "Setting the model's training or validation state.\n    "

    def begin_fit(self):
        self.run.n_epochs = 0.0
        self.run.n_iter = 0

    def after_batch(self):
        if not self.in_train:
            return
        self.run.n_epochs += 1.0 / self.iters
        self.run.n_iter += 1

    def begin_epoch(self):
        self.run.n_epochs = self.epoch
        self.model.train()
        self.run.in_train = True

    def begin_validate(self):
        self.model.eval()
        self.run.in_train = False


class TextOnlyCudaCallback(Callback):
    __doc__ = 'Putting model and variables on cuda.\n    '

    def begin_fit(self):
        self.model.cuda()

    def begin_batch(self):
        self.run.xb = self.xb.cuda()
        self.run.yb = self.yb.cuda()


class TextPlusCudaCallback(Callback):
    __doc__ = "Putting model and only the variable y on cuda.\n       Because with x in text plus mode, it's impossible to put a list of lists\n       on cuda.\n    "

    def begin_fit(self):
        self.model.cuda()

    def begin_batch(self):
        ids_input, kw_ls = list(zip(*self.xb))
        ids_input = torch.stack(ids_input).long()
        kw_ls = torch.stack(kw_ls).float()
        self.run.xb = [ids_input.cuda(), kw_ls.cuda()]
        self.run.yb = self.yb.cuda()


class Recorder(Callback):
    __doc__ = 'Saving learning rate and loss values suring the training steps, so that\n    we can plot them.\n    '

    def begin_fit(self):
        self.lrs = []
        self.losses = []

    def after_batch(self):
        if not self.in_train:
            return
        self.lrs.append(self.opt.hypers[(-1)]['lr'])
        self.losses.append(self.loss.detach().cpu())

    def plot_lr(self):
        plt.plot(self.lrs)
        plt.xlabel('Number of iteration')
        plt.ylabel('Learning rate')

    def plot_loss(self):
        plt.plot(self.losses)
        plt.xlabel('Number of iteration')
        plt.ylabel('Loss value')

    def plot(self, skip_last=0):
        losses = [o.item() for o in self.losses]
        n = len(losses) - skip_last
        plt.xscale('log')
        plt.plot(self.lrs[:n], losses[:n])
        plt.xlabel('Learning rate')
        plt.ylabel('Loss value')


class LR_Find(Callback):
    __doc__ = 'Changing the learning rate and calculating the loss at this learning rate\n    '
    _order = 1

    def __init__(self, max_iter=100, min_lr=1e-06, max_lr=10):
        self.max_iter = max_iter
        self.min_lr = min_lr
        self.max_lr = max_lr
        self.best_loss = 1000000000.0

    def begin_batch(self):
        if not self.in_train:
            return
        pos = self.n_iter / self.max_iter
        lr = self.min_lr * (self.max_lr / self.min_lr) ** pos
        for pg in self.opt.hypers:
            pg['lr'] = lr

    def after_step(self):
        if self.n_iter >= self.max_iter or self.loss > self.best_loss * 10:
            raise CancelTrainException()
        if self.loss < self.best_loss:
            self.best_loss = self.loss


class RNNTrainer(Callback):
    __doc__ = 'Returning just the decoded tensor and saving raw_ouputs and outputs.\n    Providing regularization AR, TAR\n    '

    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    def after_pred(self):
        self.raw_out = self.pred[1]
        self.out = self.pred[2]
        self.run.pred = self.pred[0]

    def after_loss(self):
        if self.alpha != 0.0:
            self.run.loss += self.alpha * self.out[(-1)].float().pow(2).mean()
        if self.beta != 0.0:
            h = self.raw_out[(-1)]
            if len(h) > 1:
                self.run.loss += self.beta * (h[:, 1:] - h[:, :-1]).float().pow(2).mean()


class ParamScheduler(Callback):
    _order = 1

    def __init__(self, pname, sched_func):
        self.pname = pname
        self.sched_func = sched_func

    def set_param(self):
        for pg in self.opt.hypers:
            pg[self.pname] = self.sched_func(self.n_epochs / self.epochs)

    def begin_batch(self):
        if self.in_train:
            self.set_param()


def annealer(f):

    def _inner(start, end):
        return partial(f, start, end)

    return _inner


@annealer
def sched_cos(start, end, pos):
    return start + (1 + math.cos(math.pi * (1 - pos))) * (end - start) / 2


def combine_scheds(pcts, scheds):
    assert sum(pcts) == 1.0
    pcts = torch.tensor([0] + listify(pcts))
    assert torch.all(pcts >= 0)
    pcts = torch.cumsum(pcts, 0)

    def _inner(pos):
        idx = (pos >= pcts).nonzero().max()
        actual_pos = (pos - pcts[idx]) / (pcts[(idx + 1)] - pcts[idx])
        return scheds[idx](actual_pos)

    return _inner