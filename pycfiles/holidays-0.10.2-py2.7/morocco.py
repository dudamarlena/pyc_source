# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/morocco.py
# Compiled at: 2020-04-13 04:40:59
from datetime import date
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import SAT, SUN
from holidays.constants import JAN, MAR, MAY, JUL, AUG, NOV
from holidays.holiday_base import HolidayBase
from holidays.utils import get_gre_date
WEEKEND = (
 SAT, SUN)

class Morocco(HolidayBase):
    """
    Moroccan holidays
    Note that holidays falling on a sunday is "lost",
    it will not be moved to another day to make up for the collision.

    # Holidays after 2020: the following four moving date holidays whose exact
    # date is announced yearly are estimated (and so denoted):
    # - Eid El Fetr*
    # - Eid El Adha*
    # - 1er Moharram*
    # - Aid al Mawlid Annabawi*
    # *only if hijri-converter library is installed, otherwise a warning is
    #  raised that this holiday is missing. hijri-converter requires
    #  Python >= 3.6
    Primary sources:
    https://fr.wikipedia.org/wiki/F%C3%AAtes_et_jours_f%C3%A9ri%C3%A9s_au_Maroc
    https://www.mmsp.gov.ma/fr/pratiques.aspx?id=38
    """

    def __init__(self, **kwargs):
        self.country = 'MA'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        """
        # Function to store the holiday name in the appropriate
        # date and to shift the Public holiday in case it happens
        # on a Saturday(Weekend)
        # (NOT USED)
        def is_weekend(self, hol_date, hol_name):
            if hol_date.weekday() == FRI:
                self[hol_date] = hol_name + " [Friday]"
                self[hol_date + rd(days=+2)] = "Sunday following " + hol_name
            else:
                self[hol_date] = hol_name
        """
        self[date(year, JAN, 1)] = 'Nouvel an - Premier janvier'
        if year > 1944:
            self[date(year, JAN, 11)] = "Commémoration de la présentation du manifeste de l'indépendance"
        self[date(year, MAY, 1)] = 'Fête du Travail'
        if year > 2000:
            self[date(year, JUL, 30)] = 'Fête du Trône'
        else:
            if year > 1962:
                self[date(year, MAR, 3)] = 'Fête du Trône'
            else:
                self[date(year, NOV, 18)] = 'Fête du Trône'
            self[date(year, AUG, 14)] = 'Journée de Oued Ed-Dahab'
            self[date(year, AUG, 20)] = 'Commémoration de la révolution du Roi et du peuple'
            if year > 2000:
                self[date(year, AUG, 21)] = 'Fête de la jeunesse'
            else:
                self[date(year, JUL, 9)] = 'Fête du Trône'
            if year > 1975:
                self[date(year, NOV, 6)] = 'Marche verte'
            if year > 1956:
                self[date(year, NOV, 18)] = "Fête de l'indépendance"
            for date_obs in get_gre_date(year, 10, 1):
                hol_date = date_obs
                self[hol_date] = 'Eid al-Fitr'
                self[hol_date + rd(days=1)] = 'Eid al-Fitr'

            for date_obs in get_gre_date(year, 12, 10):
                hol_date = date_obs
                self[hol_date] = 'Eid al-Adha'
                self[hol_date + rd(days=1)] = 'Eid al-Adha'

            for date_obs in get_gre_date(year, 1, 1):
                hol_date = date_obs
                self[hol_date] = '1er Moharram'

            for date_obs in get_gre_date(year, 3, 12):
                hol_date = date_obs
                self[hol_date] = 'Aid al Mawlid Annabawi'
                self[hol_date + rd(days=1)] = 'Aid al Mawlid Annabawi'


class MA(Morocco):
    pass


class MOR(Morocco):
    pass