# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/mutacao/ntrocas.py
# Compiled at: 2019-02-12 06:31:54
# Size of source mod 2**32: 1651 bytes
__doc__ = '\nMutação dupla troca.\n\nPrograma sob licença GNU V.3.\nDesenvolvido por: E. S. Pereira.\nVersão 0.0.1.\n'
from numpy.random import randint
from numpy import array
from .mutacao import Mutacao

class NTrocas(Mutacao):
    """NTrocas"""

    def __init__(self, pmut, bits_por_intervalo):
        super(NTrocas, self).__init__(pmut)
        self.bits_por_intervalo = bits_por_intervalo

    def mutacao(self):
        """Alteração genética de membros da população usando dupla troca."""
        nmut = self.selecao()
        cromossos_totais = self.populacao[0].size
        if nmut.size != 0:
            intervalos = [[i, i + self.bits_por_intervalo] for i in range(0, cromossos_totais, self.bits_por_intervalo)]
            ninter = len(intervalos)
            for i in nmut:
                inter1 = intervalos[randint(0, ninter)]
                inter2 = intervalos[randint(0, ninter)]
                while inter1 == inter2:
                    inter2 = intervalos[randint(0, ninter)]

                self.populacao[nmut, inter1[0]:inter1[1]], self.populacao[nmut, inter2[0]:inter2[1]] = self.populacao[nmut, inter2[0]:inter2[1]][::-1], self.populacao[nmut, inter1[0]:inter1[1]][::-1]