# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/selecao/selecao.py
# Compiled at: 2019-07-10 09:21:37
# Size of source mod 2**32: 890 bytes
"""
Classe Abstrada de Seleção de Indivíduos para cruzamento.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy.random import random
from numpy import array

class Selecao:
    __doc__ = '\n    Seleciona indivíduos para cruzamento.\n    Recebe como entrada:\n        populacao - Objeto criado a partir da classe Populacao.\n    '

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