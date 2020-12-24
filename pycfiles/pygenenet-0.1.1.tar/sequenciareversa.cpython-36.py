# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/mutacao/sequenciareversa.py
# Compiled at: 2019-02-12 06:31:54
# Size of source mod 2**32: 1058 bytes
__doc__ = '\nMutação flip.\n\nPrograma sob licença GNU V.3.\nDesenvolvido por: E. S. Pereira.\nVersão 0.0.1.\n'
from numpy.random import randint
from numpy import array, newaxis
from .mutacao import Mutacao

class SequenciaReversa(Mutacao):
    """SequenciaReversa"""

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