# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/cruzamento/kpontos.py
# Compiled at: 2019-02-12 06:31:54
# Size of source mod 2**32: 1695 bytes
__doc__ = '\nCruzamento por k-pontos.\n\nPrograma sob licença GNU V.3.\nDesenvolvido por: E. S. Pereira.\nVersão 0.0.1.\n'
from numpy.random import randint, random
from numpy import array
from .cruzamento import Cruzamento, NoCompatibleIndividualSize

class KPontos(Cruzamento):
    """KPontos"""

    def __init__(self, tamanho_populacao):
        super(KPontos, self).__init__(tamanho_populacao)

    def cruzamento(self, progenitor1, progenitor2):
        """
        Cruzamento via k-pontos de dois indivíduos.

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
        desc1 = progenitor1.copy()
        desc2 = progenitor2.copy()
        kp = randint(1, n1 - 2)
        k = []
        while len(k) <= kp:
            p = randint(1, n1 - 1)
            if p not in k:
                k.append(p)

        k.sort()
        troca = randint(0, 1)
        for i in range(kp):
            if troca == 0:
                troca = 1
            else:
                troca = 0
                desc1[k[i]:k[(i + 1)]] = progenitor2[k[i]:k[(i + 1)]]
                desc2[k[i]:k[(i + 1)]] = progenitor1[k[i]:k[(i + 1)]]

        return (desc1, desc2)