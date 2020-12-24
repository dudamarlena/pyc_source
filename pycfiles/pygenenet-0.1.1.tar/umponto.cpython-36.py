# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/cruzamento/umponto.py
# Compiled at: 2019-02-12 06:31:54
# Size of source mod 2**32: 1353 bytes
__doc__ = '\nCruzamento por por um ponto.\n\nPrograma sob licença GNU V.3.\nDesenvolvido por: E. S. Pereira.\nVersão 0.0.1.\n'
from numpy.random import randint
from numpy import array
from .cruzamento import Cruzamento, NoCompatibleIndividualSize

class UmPonto(Cruzamento):
    """UmPonto"""

    def __init__(self, tamanho_populacao):
        super(UmPonto, self).__init__(tamanho_populacao)

    def cruzamento(selfself, progenitor1, progenitor2):
        """
        Cruzamento de dois indivíduos via um pontos.

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
        ponto = randint(1, n1 - 1)
        desc1 = progenitor1.copy()
        desc2 = progenitor2.copy()
        desc1[ponto:] = progenitor2[ponto:]
        desc2[ponto:] = progenitor1[ponto:]
        return (
         desc1, desc2)