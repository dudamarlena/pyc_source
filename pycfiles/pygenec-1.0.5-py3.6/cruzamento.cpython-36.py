# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/cruzamento/cruzamento.py
# Compiled at: 2019-02-12 06:31:54
# Size of source mod 2**32: 1614 bytes
"""
Cruzamento.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy.random import randint, random
from numpy import array

class NoCompatibleIndividualSize(Exception):
    pass


class Cruzamento:
    __doc__ = '\n    Classe abstrata representando o cruzamento.\n\n    Entrada:\n        tamanho_populacao - Tamanho final da população resultante.\n    '

    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao

    def cruzamento(self, progenitor1, progenitor2):
        raise NotImplementedError('A ser implementado')

    def descendentes(self, subpopulacao, pcruz):
        """
        Retorna uma nova população de tamanho tamanho_populacao
        através do cruzamento usando k-pontos.

        Entrada:
            subpopulacao - Vetor contendo indivíduos para serem selecionados
                           para cruzamento.
            pcruz - probabilidade de cruzamento entre dois indivíduos
                    selecionados.
        """
        nova_populacao = []
        npop = len(subpopulacao)
        while len(nova_populacao) < self.tamanho_populacao - 1:
            i = randint(0, npop - 1)
            j = randint(0, npop - 1)
            while j == i:
                j = randint(0, npop - 1)

            cruzar = random()
            if cruzar < pcruz:
                desc1, desc2 = self.cruzamento(subpopulacao[i], subpopulacao[j])
                nova_populacao.append(desc1)
                nova_populacao.append(desc2)

        return array(nova_populacao)