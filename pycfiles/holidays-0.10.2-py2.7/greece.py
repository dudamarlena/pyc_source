# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/greece.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter, EASTER_ORTHODOX
from dateutil.relativedelta import relativedelta as rd, WE
from holidays.constants import JAN, MAR, MAY, AUG, OCT, DEC
from holidays.holiday_base import HolidayBase

class Greece(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'GR'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        eday = easter(year, method=EASTER_ORTHODOX)
        self[date(year, JAN, 1)] = "Πρωτοχρονιά [New Year's Day]"
        self[date(year, JAN, 6)] = 'Θεοφάνεια [Epiphany]'
        self[eday - rd(days=48)] = 'Καθαρά Δευτέρα [Clean Monday]'
        self[date(year, MAR, 25)] = 'Εικοστή Πέμπτη Μαρτίου [Independence Day]'
        self[eday + rd(days=1)] = 'Δευτέρα του Πάσχα [Easter Monday]'
        self[date(year, MAY, 1)] = 'Εργατική Πρωτομαγιά [Labour day]'
        self[eday + rd(days=50)] = 'Δευτέρα του Αγίου Πνεύματος [Monday of the Holy Spirit]'
        self[date(year, AUG, 15)] = 'Κοίμηση της Θεοτόκου [Assumption of Mary]'
        self[date(year, OCT, 28)] = 'Ημέρα του Όχι [Ochi Day]'
        self[date(year, DEC, 25)] = 'Χριστούγεννα [Christmas]'
        self[date(year, DEC, 26)] = 'Επόμενη ημέρα των Χριστουγέννων [Day after Christmas]'


class GR(Greece):
    pass


class GRC(Greece):
    pass