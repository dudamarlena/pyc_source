# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/evolucao.py
# Compiled at: 2020-01-30 09:43:57
# Size of source mod 2**32: 3165 bytes
"""
Evolução.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy.random import random

class Evolucao:
    __doc__ = '\n    Usando operadores genéticos, coloca uma população para evoluir.\n\n    Entrada:\n        populacao - Objeto do tipo Populacao\n        selecao - Objeto do tipo Selecao\n        cruzamento - Objeto do tipo cruzamento\n        mutacao - Objeto do tipo  Mutacao.\n    '

    def __init__(self, populacao, selecao, cruzamento, mutacao):
        self.populacao = populacao
        self.selecao = selecao
        self.cruzamento = cruzamento
        self.mutacao = mutacao
        self._melhor_solucao = None
        self._geracao = 0
        self._nsele = None
        self._pcruz = None
        self._epidemia = None
        self._manter_melhor = True
        self._fitness = None
        self._first = True

    def _set_epidemia(self, epidemia):
        self._epidemia = epidemia

    def _set_manter_melhor(self, manter):
        self._manter_melhor = manter

    def _get_manter_melhor(self):
        return self._manter_melhor

    def _get_epidemia(self):
        return self._epidemia

    def _set_nsele(self, nsele):
        self._nsele = nsele

    def _get_nsele(self):
        return self._nsele

    def _set_pcruz(self, pcruz):
        self._pcruz = pcruz

    def _get_pcruz(self):
        return self._pcruz

    def _get_first(self):
        return self._first

    def _set_first(self, first):
        self._first = first

    @property
    def melhor_solucao(self):
        return self._melhor_solucao

    @property
    def geracao(self):
        return self._geracao

    def evoluir(self):
        """
        Evolução elitista, por uma geração, da popução.
        """
        if self._first is True:
            self._fitness = self.populacao.avaliar()
            self._first = False
        else:
            self._melhor_solucao = self.populacao.populacao[(-1)].copy()
            subpopulacao = self.selecao.selecao((self._nsele), fitness=(self._fitness))
            populacao = self.cruzamento.descendentes(subpopulacao, pcruz=(self._pcruz))
            self.mutacao.populacao = populacao
            self.mutacao.mutacao()
            self.populacao.populacao[:] = populacao[:]
            self._geracao += 1
            if self._epidemia is not None:
                if self._geracao % self._epidemia == 0:
                    if random() < 0.8:
                        print('Epidemia')
                        self._possivel_local = 0
                        self.populacao.gerar_populacao()
            if self._manter_melhor is True:
                self.populacao.populacao[0] = self._melhor_solucao
        self._fitness = self.populacao.avaliar()
        return (
         self._fitness.min(), self._fitness.max())

    nsele = property(_get_nsele, _set_nsele)
    pcruz = property(_get_pcruz, _set_pcruz)
    epidemia = property(_get_epidemia, _set_epidemia)
    manter_melhor = property(_get_manter_melhor, _set_manter_melhor)
    first = property(_get_first, _set_first)