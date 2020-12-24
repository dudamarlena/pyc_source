# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/selecao/roleta.py
# Compiled at: 2019-07-10 09:21:21
# Size of source mod 2**32: 1101 bytes
"""
Roleta de Seleção de Indivíduos para cruzamento.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy.random import random
from numpy import array
from .selecao import Selecao

class Roleta(Selecao):
    __doc__ = '\n    Seleciona indivíduos para cruzamento usando\n    roleta de seleção.\n    Recebe como entrada:\n        populacao - Objeto criado a partir da classe Populacao.\n    '

    def __init__(self, populacao):
        super(Roleta, self).__init__(populacao)

    def selecionar(self, fitness):
        """Roleta de seleção de indivíduos."""
        if fitness is None:
            fitness = self.populacao.avaliar()
        fmin = fitness.min()
        fitness = fitness - fmin
        total = fitness.sum()
        parada = total * (1.0 - random())
        parcial = 0
        i = 0
        while True:
            if i > fitness.size - 1:
                break
            parcial += fitness[i]
            if parcial >= parada:
                break
            i += 1

        return i - 1