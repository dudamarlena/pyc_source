# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python3/pracmln/mln/methods.py
# Compiled at: 2018-04-24 04:48:32
# Size of source mod 2**32: 5624 bytes
from .inference.gibbs import GibbsSampler
from .inference.mcsat import MCSAT
from .inference.exact import EnumerationAsk
from .inference.wcspinfer import WCSPInference
from .inference.maxwalk import SAMaxWalkSAT
from .learning.cll import CLL, DCLL
from .learning.ll import LL
from .learning.bpll import BPLL, DPLL, BPLL_CG, DBPLL_CG

class Enum(object):

    def __init__(self, items):
        self.id2name = dict([(clazz.__name__, name) for clazz, name in items])
        self.name2id = dict([(name, clazz.__name__) for clazz, name in items])
        self.id2clazz = dict([(clazz.__name__, clazz) for clazz, _ in items])

    def __getattr__(self, id_):
        if id_ in self.id2clazz:
            return self.id2clazz[id_]
        raise KeyError('Enum does not define %s, only %s' % (id_, list(self.id2clazz.keys())))

    def clazz(self, key):
        if type(key).__name__ == 'type':
            key = key.__name__
        if key in self.id2clazz:
            return self.id2clazz[str(key)]
        else:
            return self.id2clazz[self.name2id[key]]
        raise KeyError('No such element "%s"' % key)

    def id(self, key):
        if type(key).__name__ == 'type':
            return key.__name__
        if key in self.name2id:
            return self.name2id[key]
        raise KeyError('No such element "%s"' % key)

    def name(self, id_):
        if id_ in self.id2name:
            return self.id2name[id_]
        raise KeyError('No element with id "%s"' % id_)

    def names(self):
        return list(self.id2name.values())

    def ids(self):
        return list(self.id2name.keys())


InferenceMethods = Enum((
 (
  GibbsSampler, 'Gibbs sampling'),
 (
  MCSAT, 'MC-SAT'),
 (
  EnumerationAsk, 'Enumeration-Ask (exact)'),
 (
  WCSPInference, 'WCSP (exact MPE with toulbar2)'),
 (
  SAMaxWalkSAT, 'Max-Walk-SAT with simulated annealing (approx. MPE)')))
LearningMethods = Enum((
 (
  CLL, 'composite-log-likelihood'),
 (
  DCLL, '[discriminative] composite-log-likelihood'),
 (
  LL, 'log-likelihood'),
 (
  DPLL, '[discriminative] pseudo-log-likelihood'),
 (
  BPLL, 'pseudo-log-likelihood'),
 (
  BPLL_CG, 'pseudo-log-likelihood (fast conjunction grounding)'),
 (
  DBPLL_CG, '[discriminative] pseudo-log-likelihood (fast conjunction grounding)')))
if __name__ == '__main__':
    print(InferenceMethods.id2clazz)
    print(InferenceMethods.id2name)
    print(InferenceMethods.name2id)
    print(LearningMethods.names())
    print(InferenceMethods.clazz(MCSAT))
    print(InferenceMethods.name('WCSPInference'))