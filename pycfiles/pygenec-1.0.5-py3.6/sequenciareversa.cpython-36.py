# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/mutacao/sequenciareversa.py
# Compiled at: 2019-02-12 06:31:54
# Size of source mod 2**32: 1058 bytes
"""
Mutação flip.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy.random import randint
from numpy import array, newaxis
from .mutacao import Mutacao

class SequenciaReversa(Mutacao):
    __doc__ = '\n    Mutaçao flip.\n\n    Entrada:\n        populacao - vetor de população que deverá sofrer mutação.\n        pmut - probabilidade de ocorrer uma mutação.\n    '

    def __init__(self, pmut):
        super(SequenciaReversa, self).__init__(pmut)

    def mutacao(self):
        """
        Alteração genética de membros da população usando sequência reversa.
        """
        nmut = self.selecao()
        if nmut.size != 0:
            for k in nmut:
                i = randint(0, self.ngen - 1)
                j = randint(0, self.ngen - 1)
                while i == j:
                    j = randint(0, self.ngen - 1)

                if i > j:
                    i, j = j, i
                self.populacao[k, i:j] = self.populacao[k, i:j][::-1]