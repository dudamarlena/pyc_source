# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/mutacao/mutacao.py
# Compiled at: 2019-02-12 06:31:54
# Size of source mod 2**32: 986 bytes
"""
Mutação.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy.random import randint, random
from numpy import array

class Mutacao:
    __doc__ = '\n    Classe base para operadores de mutação:\n    Entrada:\n        pmut - probabilidade de ocorrer uma mutação.\n    '

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