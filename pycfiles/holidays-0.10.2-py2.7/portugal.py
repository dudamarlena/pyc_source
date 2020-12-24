# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/portugal.py
# Compiled at: 2020-02-11 16:32:11
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class Portugal(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'PT'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Ano Novo'
        e = easter(year)
        self[e - rd(days=2)] = 'Sexta-feira Santa'
        self[e] = 'Páscoa'
        if year < 2013 or year > 2015:
            self[e + rd(days=60)] = 'Corpo de Deus'
            self[date(year, OCT, 5)] = 'Implantação da República'
            self[date(year, NOV, 1)] = 'Dia de Todos os Santos'
            self[date(year, DEC, 1)] = 'Restauração da Independência'
        self[date(year, 4, 25)] = 'Dia da Liberdade'
        self[date(year, 5, 1)] = 'Dia do Trabalhador'
        self[date(year, 6, 10)] = 'Dia de Portugal'
        self[date(year, 8, 15)] = 'Assunção de Nossa Senhora'
        self[date(year, DEC, 8)] = 'Imaculada Conceição'
        self[date(year, DEC, 25)] = 'Dia de Natal'


class PT(Portugal):
    pass


class PRT(Portugal):
    pass


class PortugalExt(Portugal):
    """
    Adds extended days that most people have as a bonus from their companies:
    - Carnival
    - the day before and after xmas
    - the day before the new year
    - Lisbon's city holiday
    """

    def _populate(self, year):
        super(PortugalExt, self)._populate(year)
        e = easter(year)
        self[e - rd(days=47)] = 'Carnaval'
        self[date(year, DEC, 24)] = 'Véspera de Natal'
        self[date(year, DEC, 26)] = '26 de Dezembro'
        self[date(year, DEC, 31)] = 'Véspera de Ano Novo'
        self[date(year, 6, 13)] = 'Dia de Santo António'


class PTE(PortugalExt):
    pass


class PRTE(PortugalExt):
    pass