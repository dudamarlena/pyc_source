# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/cruzamento/fatias.py
# Compiled at: 2019-08-16 08:51:16
# Size of source mod 2**32: 2520 bytes
"""
Cruzamento via embaralhamento.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy.random import shuffle, randint
from numpy import concatenate
from .cruzamento import Cruzamento, NoCompatibleIndividualSize

class Fatias(Cruzamento):
    __doc__ = '\n    Gerador de população via embaralhanmento e cruzamento de um ponto.\n\n    Entrada:\n        tamanho_populacao - Tamanho final da população resultante.\n    '

    def __init__(self, tamanho_populacao, pontos):
        super(Fatias, self).__init__(tamanho_populacao)
        self._pontos = pontos

    def cruzamento(self, progenitor1, progenitor2):
        """
        Cruzamento de dois indivíduos via embaralhanmento um pontos.
        Os genes são fatiados e o cruzamento é realizado para cada fatia de
        forma distinta.

        Entrada:
            ind1 - Primeiro indivíduo
            ind2 - Segundo indivíduo
        O tamanho de ambos os indivíduos deve ser igual, do contrário um erro
        será levantado.
        """
        desc1 = []
        desc2 = []
        for i in range(1, len(self._pontos)):
            i0, i1 = self._pontos[(i - 1)], self._pontos[i]
            tmp1, tmp2 = self._embaralhamento(progenitor1[i0:i1], progenitor2[i0:i1])
            desc1.append(tmp1)
            desc2.append(tmp2)

        return (
         concatenate(desc1), concatenate(desc2))

    def _embaralhamento(self, progenitor1, progenitor2):
        """
        Cruzamento de dois indivíduos via embaralhanmento um pontos.

        Entrada:
            ind1 - Primeiro indivíduo
            ind2 - Segundo indivíduo
        O tamanho de ambos os indivíduos deve ser igual, do contrário um erro
        será levantado.
        """
        n1 = len(progenitor1)
        n2 = len(progenitor2)
        if n1 != n2:
            msg = 'Tamanho ind1 {0} diferente de ind2 {1}'.format(n1, n2)
            raise NoCompatibleIndividualSize(msg)
        order = list(range(n1))
        shuffle(order)
        ponto = randint(1, n1 - 1)
        desc1 = progenitor1.copy()
        desc2 = progenitor2.copy()
        desc1[:] = desc1[order]
        desc2[:] = desc2[order]
        desc1[ponto:], desc2[ponto:] = desc2[ponto:], desc1[ponto:]
        tmp1 = desc1.copy()
        tmp2 = desc2.copy()
        for i, j in enumerate(order):
            desc1[j] = tmp1[i]
            desc2[j] = tmp2[i]

        return (desc1, desc2)