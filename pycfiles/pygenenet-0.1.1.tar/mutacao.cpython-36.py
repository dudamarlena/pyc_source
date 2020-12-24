# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/mutacao/mutacao.py
# Compiled at: 2019-02-12 06:31:54
# Size of source mod 2**32: 986 bytes
__doc__ = '\nMutação.\n\nPrograma sob licença GNU V.3.\nDesenvolvido por: E. S. Pereira.\nVersão 0.0.1.\n'
from numpy.random import randint, random
from numpy import array

class Mutacao:
    """Mutacao"""

    def __init__(self, pmut):
        self.pmut = pmut
        self._populacao = None
        self.npop = None
        self.ngen = None

    def _set_populacao(self, populacao):
        self._populacao = populacao
        self.npop = self._populacao.shape[0]
        self.ngen = self._populacao.shape[1]

    def _get_populacao(self):
        return self._populacao

    def selecao(self):
        nmut = array([i for i in range(self.npop) if random() < self.pmut])
        return nmut

    def mutacao(self):
        raise NotImplementedError('A ser implementado')

    populacao = property(_get_populacao, _set_populacao)