# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/selecao/classificacao.py
# Compiled at: 2019-07-10 09:22:03
# Size of source mod 2**32: 1123 bytes
"""
Roleta de Seleção de Indivíduos para cruzamento, classificação.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy.random import random
from numpy import array, argsort
from .selecao import Selecao

class Classificacao(Selecao):
    __doc__ = '\n    Seleciona indivíduos para cruzamento usando\n    Classificação.\n    Recebe como entrada:\n        populacao - Objeto criado a partir da classe Populacao.\n    '

    def __init__(self, populacao):
        super(Classificacao, self).__init__(populacao)

    def selecionar(self, fitness):
        """Roleta de seleção de indivíduos."""
        if fitness is None:
            fitness = self.populacao.avaliar()
        classificacao = argsort(fitness) + 1
        total = classificacao.sum()
        parada = total * random()
        parcial = 0
        i = 0
        while True:
            if i > fitness.size - 1:
                break
            parcial += classificacao[i]
            if parcial >= parada:
                break
            i += 1

        return i - 1