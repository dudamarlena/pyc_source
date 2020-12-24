# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/populacao.py
# Compiled at: 2020-01-30 09:04:47
# Size of source mod 2**32: 1550 bytes
"""
Gerador aleatório de população.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy.random import randint
from numpy import argsort, unique

class Populacao:
    __doc__ = '\n    Cria e avalia uma população.\n    Recebe como entrada:\n        avaliacao - Função que recebe um indivíduo como entrada e retorna\n                    um valor numérico.\n        cromossos_totais - Numero inteiro representando o tamanho da cadeia\n                           genética do indivíduo.\n        tamanho_populacao - Numero inteiro representando o número total de\n                            indivíduos na população.\n    '

    def __init__(self, avaliacao, genes_totais, tamanho_populacao):
        self.avaliacao = avaliacao
        self.genes_totais = genes_totais
        self.tamanho_populacao = tamanho_populacao
        self.gerar_populacao()

    def gerar_populacao(self):
        """Gerador aleatório de população."""
        self.populacao = randint(0, 2, size=(self.tamanho_populacao,
         self.genes_totais),
          dtype='b')

    def avaliar(self):
        """Avalia e ordena a população."""
        u, indices = unique((self.populacao), return_inverse=True, axis=0)
        valores = self.avaliacao(u)
        valores = valores[indices]
        ind = argsort(valores)
        self.populacao[:] = self.populacao[ind]
        valores = valores[ind]
        return valores[ind]