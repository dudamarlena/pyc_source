# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/selecao/torneio.py
# Compiled at: 2019-07-10 09:21:48
# Size of source mod 2**32: 910 bytes
__doc__ = '\nRoleta de Seleção de Indivíduos para cruzamento.\n\nPrograma sob licença GNU V.3.\nDesenvolvido por: E. S. Pereira.\nVersão 0.0.1.\n'
from numpy.random import choice
from numpy import array, where
from .selecao import Selecao

class Torneio(Selecao):
    """Torneio"""

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