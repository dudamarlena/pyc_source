# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/france.py
# Compiled at: 2020-02-11 14:52:08
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class France(HolidayBase):
    """Official French holidays.

    Some provinces have specific holidays, only those are included in the
    PROVINCES, because these provinces have different administrative status,
    which makes it difficult to enumerate.

    For religious holidays usually happening on Sundays (Easter, Pentecost),
    only the following Monday is considered a holiday.

    Primary sources:
        https://fr.wikipedia.org/wiki/Fêtes_et_jours_fériés_en_France
        https://www.service-public.fr/particuliers/vosdroits/F2405
    """
    PROVINCES = [
     'Métropole', 'Alsace-Moselle', 'Guadeloupe', 'Guyane',
     'Martinique', 'Mayotte', 'Nouvelle-Calédonie', 'La Réunion',
     'Polynésie Française', 'Saint-Barthélémy', 'Saint-Martin',
     'Wallis-et-Futuna']

    def __init__(self, **kwargs):
        self.country = 'FR'
        self.prov = kwargs.pop('prov', 'Métropole')
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year > 1810:
            self[date(year, JAN, 1)] = "Jour de l'an"
        if year > 1919:
            name = 'Fête du Travail'
            if year <= 1948:
                name += ' et de la Concorde sociale'
            self[date(year, MAY, 1)] = name
        if 1953 <= year <= 1959 or year > 1981:
            self[date(year, MAY, 8)] = 'Armistice 1945'
        if year >= 1880:
            self[date(year, JUL, 14)] = 'Fête nationale'
        if year >= 1918:
            self[date(year, NOV, 11)] = 'Armistice 1918'
        if self.prov in ('Alsace-Moselle', 'Guadeloupe', 'Guyane', 'Martinique', 'Polynésie Française'):
            self[easter(year) - rd(days=2)] = 'Vendredi saint'
        if self.prov == 'Alsace-Moselle':
            self[date(year, DEC, 26)] = 'Deuxième jour de Noël'
        if year >= 1886:
            self[easter(year) + rd(days=1)] = 'Lundi de Pâques'
            self[easter(year) + rd(days=50)] = 'Lundi de Pentecôte'
        if year >= 1802:
            self[easter(year) + rd(days=39)] = 'Ascension'
            self[date(year, AUG, 15)] = 'Assomption'
            self[date(year, NOV, 1)] = 'Toussaint'
            name = 'Noël'
            if self.prov == 'Alsace-Moselle':
                name = 'Premier jour de ' + name
            self[date(year, DEC, 25)] = name
        if self.prov == 'Mayotte':
            self[date(year, APR, 27)] = "Abolition de l'esclavage"
        if self.prov == 'Wallis-et-Futuna':
            self[date(year, APR, 28)] = 'Saint Pierre Chanel'
        if self.prov == 'Martinique':
            self[date(year, MAY, 22)] = "Abolition de l'esclavage"
        if self.prov in ('Guadeloupe', 'Saint-Martin'):
            self[date(year, MAY, 27)] = "Abolition de l'esclavage"
        if self.prov == 'Guyane':
            self[date(year, JUN, 10)] = "Abolition de l'esclavage"
        if self.prov == 'Polynésie Française':
            self[date(year, JUN, 29)] = "Fête de l'autonomie"
        if self.prov in ('Guadeloupe', 'Martinique'):
            self[date(year, JUL, 21)] = 'Fête Victor Schoelcher'
        if self.prov == 'Wallis-et-Futuna':
            self[date(year, JUL, 29)] = 'Fête du Territoire'
        if self.prov == 'Nouvelle-Calédonie':
            self[date(year, SEP, 24)] = 'Fête de la Citoyenneté'
        if self.prov == 'Saint-Barthélémy':
            self[date(year, OCT, 9)] = "Abolition de l'esclavage"
        if self.prov == 'La Réunion' and year >= 1981:
            self[date(year, DEC, 20)] = "Abolition de l'esclavage"


class FRA(France):
    pass