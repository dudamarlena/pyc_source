# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/selecao/roleta.py
# Compiled at: 2019-07-10 09:21:21
# Size of source mod 2**32: 1101 bytes
__doc__ = '\nRoleta de Seleção de Indivíduos para cruzamento.\n\nPrograma sob licença GNU V.3.\nDesenvolvido por: E. S. Pereira.\nVersão 0.0.1.\n'
from numpy.random import random
from numpy import array
from .selecao import Selecao

class Roleta(Selecao):
    """Roleta"""

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