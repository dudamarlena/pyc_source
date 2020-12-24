# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/populacao.py
# Compiled at: 2020-01-30 09:04:47
# Size of source mod 2**32: 1550 bytes
__doc__ = '\nGerador aleatório de população.\n\nPrograma sob licença GNU V.3.\nDesenvolvido por: E. S. Pereira.\nVersão 0.0.1.\n'
from numpy.random import randint
from numpy import argsort, unique

class Populacao:
    """Populacao"""

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