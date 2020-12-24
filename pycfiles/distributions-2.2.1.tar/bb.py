# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: distributions/dbg/models/bb.py
# Compiled at: 2017-10-28 18:53:45
from distributions.dbg.special import log, gammaln
from distributions.dbg.random import sample_bernoulli, sample_beta
from distributions.mixins import SharedMixin, GroupIoMixin, SharedIoMixin
NAME = 'BetaBernoulli'
EXAMPLES = [
 {'shared': {'alpha': 0.5, 'beta': 2.0}, 'values': [
             False, False, True, False, True, True, False, False]},
 {'shared': {'alpha': 10.5, 'beta': 0.5}, 'values': [
             False, False, False, False, False, False, False, True]}]
Value = bool

class Shared(SharedMixin, SharedIoMixin):

    def __init__(self):
        self.alpha = None
        self.beta = None
        return

    def load(self, raw):
        self.alpha = float(raw['alpha'])
        self.beta = float(raw['beta'])

    def dump(self):
        return {'alpha': self.alpha, 
           'beta': self.beta}

    def protobuf_load(self, message):
        self.alpha = float(message.alpha)
        self.beta = float(message.beta)

    def protobuf_dump(self, message):
        message.alpha = self.alpha
        message.beta = self.beta


class Group(GroupIoMixin):

    def __init__(self):
        self.heads = None
        self.tails = None
        return

    def init(self, shared):
        self.heads = 0
        self.tails = 0

    def add_value(self, shared, value):
        if value:
            self.heads += 1
        else:
            self.tails += 1

    def add_repeated_value(self, shared, value, count):
        if value:
            self.heads += count
        else:
            self.tails += count

    def remove_value(self, shared, value):
        if value:
            self.heads -= 1
        else:
            self.tails -= 1

    def merge(self, shared, source):
        self.heads += source.heads
        self.tails += source.tails

    def score_value(self, shared, value):
        r"""
        \cite{wallach2009rethinking} Eqn 4.
        McCallum, et. al, 'Rething LDA: Why Priors Matter'
        """
        heads = shared.alpha + self.heads
        tails = shared.beta + self.tails
        numer = heads if value else tails
        denom = heads + tails
        return log(numer / denom)

    def score_data(self, shared):
        r"""
        \cite{jordan2001more} Eqn 22.
        Michael Jordan's CS281B/Stat241B
        Advanced Topics in Learning and Decision Making course,
        'More on Marginal Likelihood'
        """
        alpha = shared.alpha + self.heads
        beta = shared.beta + self.tails
        score = gammaln(shared.alpha + shared.beta) - gammaln(alpha + beta)
        score += gammaln(alpha) - gammaln(shared.alpha)
        score += gammaln(beta) - gammaln(shared.beta)
        return score

    def sample_value(self, shared):
        sampler = Sampler()
        sampler.init(shared, self)
        return sampler.eval(shared)

    def load(self, raw):
        self.heads = raw['heads']
        self.tails = raw['tails']

    def dump(self):
        return {'heads': self.heads, 
           'tails': self.tails}

    def protobuf_load(self, message):
        self.heads = message.heads
        self.tails = message.tails

    def protobuf_dump(self, message):
        message.heads = self.heads
        message.tails = self.tails


class Sampler(object):

    def init(self, shared, group=None):
        if group is None:
            self.p = sample_beta(shared.alpha, shared.beta)
        else:
            alpha = shared.alpha + group.heads
            beta = shared.beta + group.tails
            self.p = sample_beta(alpha, beta)
        return

    def eval(self, shared):
        return sample_bernoulli(self.p)


def sample_group(shared, size):
    group = Group()
    group.init(shared)
    sampler = Sampler()
    sampler.init(shared, group)
    return [ sampler.eval(shared) for _ in xrange(size) ]