# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/mutacao/duplatroca.py
# Compiled at: 2019-02-12 06:31:54
# Size of source mod 2**32: 974 bytes
__doc__ = '\nMutação dupla troca.\n\nPrograma sob licença GNU V.3.\nDesenvolvido por: E. S. Pereira.\nVersão 0.0.1.\n'
from numpy.random import randint
from numpy import array
from .mutacao import Mutacao

class DuplaTroca(Mutacao):
    """DuplaTroca"""

    def __init__(self, pmut):
        super(DuplaTroca, self).__init__(pmut)

    def mutacao(self):
        """Alteração genética de membros da população usando dupla troca."""
        nmut = self.selecao()
        if nmut.size != 0:
            gen1 = array([randint(0, self.ngen - 1) for _ in nmut])
            gen2 = array([randint(0, self.ngen - 1) for _ in nmut])
            self.populacao[(nmut, gen1)], self.populacao[(nmut, gen2)] = self.populacao[(nmut, gen2)], self.populacao[(nmut, gen1)]