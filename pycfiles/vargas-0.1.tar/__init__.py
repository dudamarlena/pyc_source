# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gabriel.falcao/Projetos/vargas/vargas/__init__.py
# Compiled at: 2010-12-26 21:15:37
from datetime import datetime
version = '0.1'
plural_de = lambda singular, plural, numero: numero > 1 and plural or singular

class Restante(object):

    def __init__(self, valor, unidade):
        self.valor = valor
        self.unidade = unidade

    @property
    def pouco_mais_de_1_minuto(self):
        if self.valor < 5 and self.unidade == 'minuto':
            return True
        if self.valor < 60 and self.unidade == 'segundos':
            return True
        return False

    @property
    def meia_hora(self):
        if self.valor == 30 and self.unidade == 'minutos':
            return True
        return False

    @property
    def string(self):
        if self.valor > 0:
            return ' e %d %s' % (self.valor, self.unidade)
        return ''


class TempoRelativo(object):
    possibilidades = (
     (
      31536000, lambda n: plural_de('ano', 'anos', n)),
     (
      2592000, lambda n: plural_de('mês', 'meses', n)),
     (
      604800, lambda n: plural_de('semana', 'semanas', n)),
     (
      86400, lambda n: plural_de('dia', 'dias', n)),
     (
      3600, lambda n: plural_de('hora', 'horas', n)),
     (
      60, lambda n: plural_de('minuto', 'minutos', n)))

    def __init__(self, anterior):
        self.now = datetime.now()
        self.anterior = anterior
        self.delta = self.now - self.anterior
        self.decorrido = self.delta.days * 24 * 60 * 60 + self.delta.seconds

    @property
    def string(self):
        for (total, (segundos, unidade_de_tempo)) in enumerate(self.possibilidades):
            restante = None
            if self.decorrido >= segundos:
                valor = int(self.decorrido / segundos)
                string = '%d %s' % (valor, unidade_de_tempo(valor))
                extra = float(self.decorrido) / segundos > valor
                proximo = total + 1
                if extra:
                    sobra = self.decorrido - segundos * valor
                    if len(self.possibilidades) > proximo:
                        (segundos_restantes, unidade_restante) = self.possibilidades[proximo]
                        valor_restante = sobra / segundos_restantes
                        restante = Restante(valor_restante, unidade_restante(valor_restante))
                    else:
                        restante = Restante(sobra, plural_de('segundo', 'segundos', sobra))
                return (string, restante)

        return

    @property
    def ha(self):
        if self.decorrido < 60:
            return 'há menos de um minuto'
        (string, restante) = self.string
        predicado = ''
        if restante:
            if restante.pouco_mais_de_1_minuto:
                predicado = ' pouco mais de'
            elif restante.meia_hora:
                string += ' e meia'
            else:
                string += restante.string
        return 'há%s %s' % (predicado, string)

    @property
    def atras(self):
        if self.decorrido < 60:
            return 'alguns segundos atrás'
        (string, restante) = self.string
        if restante:
            string += restante.string
        return '%s atrás' % string

    def __unicode__(self):
        return self.ha

    def __repr__(self):
        return self.atras