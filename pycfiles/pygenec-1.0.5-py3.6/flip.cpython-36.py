# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/mutacao/flip.py
# Compiled at: 2019-02-12 06:31:54
# Size of source mod 2**32: 823 bytes
"""
Mutação flip.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy.random import randint
from numpy import array
from .mutacao import Mutacao

class Flip(Mutacao):
    __doc__ = '\n    Mutaçao flip.\n\n    Entrada:\n        populacao - vetor de população que deverá sofrer mutação.\n        pmut - probabilidade de ocorrer uma mutação.\n    '

    def __init__(self, pmut):
        super(Flip, self).__init__(pmut)

    def mutacao(self):
        """Alteração genética de membros da população usando mutação flip."""
        nmut = self.selecao()
        if nmut.size != 0:
            genflip = array([randint(0, self.ngen - 1) for _ in nmut])
            self.populacao[(nmut, genflip)] = 1 - self.populacao[(nmut, genflip)]