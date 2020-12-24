# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/selecao/selecao.py
# Compiled at: 2019-07-10 09:21:37
# Size of source mod 2**32: 890 bytes
__doc__ = '\nClasse Abstrada de Seleção de Indivíduos para cruzamento.\n\nPrograma sob licença GNU V.3.\nDesenvolvido por: E. S. Pereira.\nVersão 0.0.1.\n'
from numpy.random import random
from numpy import array

class Selecao:
    """Selecao"""

    def __init__(self, populacao):
        self.populacao = populacao

    def selecionar(self, fitness=None):
        raise NotImplementedError('A ser implementado')

    def selecao(self, n, fitness=None):
        """
        Retorna uma população de tamanho n,
        selecionanda via roleta.
        """
        progenitores = array([self.selecionar(fitness) for _ in range(n)])
        return self.populacao.populacao[progenitores]