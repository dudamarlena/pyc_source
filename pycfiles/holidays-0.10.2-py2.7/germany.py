# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/germany.py
# Compiled at: 2020-03-21 18:46:42
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, WE
from holidays.constants import JAN, MAR, MAY, AUG, SEP, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class Germany(HolidayBase):
    """Official holidays for Germany in its current form.

    This class doesn't return any holidays before 1990-10-03.

    Before that date the current Germany was separated into the "German
    Democratic Republic" and the "Federal Republic of Germany" which both had
    somewhat different holidays. Since this class is called "Germany" it
    doesn't really make sense to include the days from the two former
    countries.

    Note that Germany doesn't have rules for holidays that happen on a
    Sunday. Those holidays are still holiday days but there is no additional
    day to make up for the "lost" day.

    Also note that German holidays are partly declared by each province there
    are some weired edge cases:

        - "Mariä Himmelfahrt" is only a holiday in Bavaria (BY) if your
          municipality is mostly catholic which in term depends on census data.
          Since we don't have this data but most municipalities in Bavaria
          *are* mostly catholic, we count that as holiday for whole Bavaria.
        - There is an "Augsburger Friedensfest" which only exists in the town
          Augsburg. This is excluded for Bavaria.
        - "Gründonnerstag" (Thursday before easter) is not a holiday but pupils
           don't have to go to school (but only in Baden Württemberg) which is
           solved by adjusting school holidays to include this day. It is
           excluded from our list.
        - "Fronleichnam" is a holiday in certain, explicitly defined
          municipalities in Saxony (SN) and Thuringia (TH). We exclude it from
          both provinces.
    """
    PROVINCES = [
     'BW', 'BY', 'BE', 'BB', 'HB', 'HH', 'HE', 'MV', 'NI', 'NW',
     'RP', 'SL', 'SN', 'ST', 'SH', 'TH']

    def __init__(self, **kwargs):
        self.country = 'DE'
        self.prov = kwargs.pop('prov', None)
        HolidayBase.__init__(self, **kwargs)
        return

    def _populate(self, year):
        if year <= 1989:
            return
        if year > 1990:
            self[date(year, JAN, 1)] = 'Neujahr'
            if self.prov in ('BW', 'BY', 'ST'):
                self[date(year, JAN, 6)] = 'Heilige Drei Könige'
            self[easter(year) - rd(days=2)] = 'Karfreitag'
            if self.prov == 'BB':
                self[easter(year)] = 'Ostersonntag'
            self[easter(year) + rd(days=1)] = 'Ostermontag'
            self[date(year, MAY, 1)] = 'Erster Mai'
            if self.prov == 'BE' and year == 2020:
                self[date(year, MAY, 8)] = '75. Jahrestag der Befreiung vom Nationalsozialismus und der Beendigung des Zweiten Weltkriegs in Europa'
            self[easter(year) + rd(days=39)] = 'Christi Himmelfahrt'
            if self.prov == 'BB':
                self[easter(year) + rd(days=49)] = 'Pfingstsonntag'
            self[easter(year) + rd(days=50)] = 'Pfingstmontag'
            if self.prov in ('BW', 'BY', 'HE', 'NW', 'RP', 'SL'):
                self[easter(year) + rd(days=60)] = 'Fronleichnam'
            if self.prov in ('BY', 'SL'):
                self[date(year, AUG, 15)] = 'Mariä Himmelfahrt'
        self[date(year, OCT, 3)] = 'Tag der Deutschen Einheit'
        if self.prov in ('BB', 'MV', 'SN', 'ST', 'TH'):
            self[date(year, OCT, 31)] = 'Reformationstag'
        if self.prov in ('HB', 'SH', 'NI', 'HH') and year >= 2018:
            self[date(year, OCT, 31)] = 'Reformationstag'
        if year == 2017:
            self[date(year, OCT, 31)] = 'Reformationstag'
        if self.prov in ('BW', 'BY', 'NW', 'RP', 'SL'):
            self[date(year, NOV, 1)] = 'Allerheiligen'
        if year <= 1994 or self.prov == 'SN':
            base_data = date(year, NOV, 23)
            weekday_delta = WE(-2) if base_data.weekday() == 2 else WE(-1)
            self[base_data + rd(weekday=weekday_delta)] = 'Buß- und Bettag'
        if year >= 2019:
            if self.prov == 'TH':
                self[date(year, SEP, 20)] = 'Weltkindertag'
            if self.prov == 'BE':
                self[date(year, MAR, 8)] = 'Internationaler Frauentag'
        self[date(year, DEC, 25)] = 'Erster Weihnachtstag'
        self[date(year, DEC, 26)] = 'Zweiter Weihnachtstag'


class DE(Germany):
    pass


class DEU(Germany):
    pass