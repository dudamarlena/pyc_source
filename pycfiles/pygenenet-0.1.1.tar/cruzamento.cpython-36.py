# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/cruzamento/cruzamento.py
# Compiled at: 2019-02-12 06:31:54
# Size of source mod 2**32: 1614 bytes
__doc__ = '\nCruzamento.\n\nPrograma sob licença GNU V.3.\nDesenvolvido por: E. S. Pereira.\nVersão 0.0.1.\n'
from numpy.random import randint, random
from numpy import array

class NoCompatibleIndividualSize(Exception):
    pass


class Cruzamento:
    """Cruzamento"""

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