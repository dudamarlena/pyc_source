# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/selecao/torneio.py
# Compiled at: 2019-07-10 09:21:48
# Size of source mod 2**32: 910 bytes
"""
Roleta de Seleção de Indivíduos para cruzamento.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy.random import choice
from numpy import array, where
from .selecao import Selecao

class Torneio(Selecao):
    __doc__ = '\n    Seleciona indivíduos para cruzamento usando\n    Torneio.\n    Recebe como entrada:\n        populacao - Objeto criado a partir da classe Populacao.\n    '

    def __init__(self, populacao, tamanho=10):
        super(Torneio, self).__init__(populacao)
        self.tamanho = tamanho

    def selecionar(self, fitness):
        """Retorna o indivíduo campeão da rodada."""
        if fitness is None:
            fitness = self.populacao.avaliar()
        grupo = choice(fitness, size=(self.tamanho))
        campeao = grupo.max()
        i = where(fitness == campeao)[0][0]
        return i