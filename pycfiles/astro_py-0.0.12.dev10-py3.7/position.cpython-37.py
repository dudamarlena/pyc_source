# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astro_py/position.py
# Compiled at: 2019-10-17 02:44:47
# Size of source mod 2**32: 8002 bytes
from flatlibfr import const

class position:
    __doc__ = ' This class is a tool for positioning over circle 360 '

    def __init__(self, asc):
        self.asc = asc

    def position_circle_360_object(self, id, sign_pos):
        """ House, aspect, planet """
        pos = self.position_circle_360_zodiac(id) + float(sign_pos)
        if pos >= 0:
            pos = pos
        else:
            pos = 360.0 + pos
        if pos == 360.0:
            pos = 0.0
        return pos

    def position_circle_360_zodiac(self, id):
        pos = (self.switch_asc(id=id) - 1) * 30.0 - self.asc.signlon
        if pos >= 0:
            pos = pos
        else:
            pos = 360.0 + pos
        if pos == 360.0:
            pos = 0.0
        return pos

    def switch_current_sign_to_id(self, sign):
        """ For house.py, current sign -> id sign """
        switcher = {const.ARIES: const.ID_ARIES, 
         const.TAURUS: const.ID_TAURUS, 
         const.GEMINI: const.ID_GEMINI, 
         const.CANCER: const.ID_CANCER, 
         const.LEO: const.ID_LEO, 
         const.VIRGO: const.ID_VIRGO, 
         const.LIBRA: const.ID_LIBRA, 
         const.SCORPIO: const.ID_SCORPIO, 
         const.SAGITTARIUS: const.ID_SAGITTARIUS, 
         const.CAPRICORN: const.ID_CAPRICORN, 
         const.AQUARIUS: const.ID_AQUARIUS, 
         const.PISCES: const.ID_PISCES}
        return switcher.get(sign, '?')

    def switch_asc(self, id):
        """ Switch case for give a number bettween 1 - 12 by ascendant """
        switcher = {const.ARIES: id, 
         const.TAURUS: self.switch_asc_taurus(id), 
         const.GEMINI: self.switch_asc_gemini(id), 
         const.CANCER: self.switch_asc_cancer(id), 
         const.LEO: self.switch_asc_leo(id), 
         const.VIRGO: self.switch_asc_virgo(id), 
         const.LIBRA: self.switch_asc_libra(id), 
         const.SCORPIO: self.switch_asc_scorpio(id), 
         const.SAGITTARIUS: self.switch_asc_sagittarius(id), 
         const.CAPRICORN: self.switch_asc_capricorn(id), 
         const.AQUARIUS: self.switch_asc_aquarius(id), 
         const.PISCES: self.switch_asc_pisces(id)}
        return switcher.get(self.asc.sign, '?')

    def switch_asc_taurus(self, id):
        switcher = {const.ID_TAURUS: 1, 
         const.ID_GEMINI: 2, 
         const.ID_CANCER: 3, 
         const.ID_LEO: 4, 
         const.ID_VIRGO: 5, 
         const.ID_LIBRA: 6, 
         const.ID_SCORPIO: 7, 
         const.ID_SAGITTARIUS: 8, 
         const.ID_CAPRICORN: 9, 
         const.ID_AQUARIUS: 10, 
         const.ID_PISCES: 11, 
         const.ID_ARIES: 12}
        return switcher.get(id, '?')

    def switch_asc_gemini(self, id):
        switcher = {const.ID_GEMINI: 1, 
         const.ID_CANCER: 2, 
         const.ID_LEO: 3, 
         const.ID_VIRGO: 4, 
         const.ID_LIBRA: 5, 
         const.ID_SCORPIO: 6, 
         const.ID_SAGITTARIUS: 7, 
         const.ID_CAPRICORN: 8, 
         const.ID_AQUARIUS: 9, 
         const.ID_PISCES: 10, 
         const.ID_ARIES: 11, 
         const.ID_TAURUS: 12}
        return switcher.get(id, '?')

    def switch_asc_cancer(self, id):
        switcher = {const.ID_CANCER: 1, 
         const.ID_LEO: 2, 
         const.ID_VIRGO: 3, 
         const.ID_LIBRA: 4, 
         const.ID_SCORPIO: 5, 
         const.ID_SAGITTARIUS: 6, 
         const.ID_CAPRICORN: 7, 
         const.ID_AQUARIUS: 8, 
         const.ID_PISCES: 9, 
         const.ID_ARIES: 10, 
         const.ID_TAURUS: 11, 
         const.ID_GEMINI: 12}
        return switcher.get(id, '?')

    def switch_asc_leo(self, id):
        switcher = {const.ID_LEO: 1, 
         const.ID_VIRGO: 2, 
         const.ID_LIBRA: 3, 
         const.ID_SCORPIO: 4, 
         const.ID_SAGITTARIUS: 5, 
         const.ID_CAPRICORN: 6, 
         const.ID_AQUARIUS: 7, 
         const.ID_PISCES: 8, 
         const.ID_ARIES: 9, 
         const.ID_TAURUS: 10, 
         const.ID_GEMINI: 11, 
         const.ID_CANCER: 12}
        return switcher.get(id, '?')

    def switch_asc_virgo(self, id):
        switcher = {const.ID_VIRGO: 1, 
         const.ID_LIBRA: 2, 
         const.ID_SCORPIO: 3, 
         const.ID_SAGITTARIUS: 4, 
         const.ID_CAPRICORN: 5, 
         const.ID_AQUARIUS: 6, 
         const.ID_PISCES: 7, 
         const.ID_ARIES: 8, 
         const.ID_TAURUS: 9, 
         const.ID_GEMINI: 10, 
         const.ID_CANCER: 11, 
         const.ID_LEO: 12}
        return switcher.get(id, '?')

    def switch_asc_libra(self, id):
        switcher = {const.ID_LIBRA: 1, 
         const.ID_SCORPIO: 2, 
         const.ID_SAGITTARIUS: 3, 
         const.ID_CAPRICORN: 4, 
         const.ID_AQUARIUS: 5, 
         const.ID_PISCES: 6, 
         const.ID_ARIES: 7, 
         const.ID_TAURUS: 8, 
         const.ID_GEMINI: 9, 
         const.ID_CANCER: 10, 
         const.ID_LEO: 11, 
         const.ID_VIRGO: 12}
        return switcher.get(id, '?')

    def switch_asc_scorpio(self, id):
        switcher = {const.ID_SCORPIO: 1, 
         const.ID_SAGITTARIUS: 2, 
         const.ID_CAPRICORN: 3, 
         const.ID_AQUARIUS: 4, 
         const.ID_PISCES: 5, 
         const.ID_ARIES: 6, 
         const.ID_TAURUS: 7, 
         const.ID_GEMINI: 8, 
         const.ID_CANCER: 9, 
         const.ID_LEO: 10, 
         const.ID_VIRGO: 11, 
         const.ID_LIBRA: 12}
        return switcher.get(id, '?')

    def switch_asc_sagittarius(self, id):
        switcher = {const.ID_SAGITTARIUS: 1, 
         const.ID_CAPRICORN: 2, 
         const.ID_AQUARIUS: 3, 
         const.ID_PISCES: 4, 
         const.ID_ARIES: 5, 
         const.ID_TAURUS: 6, 
         const.ID_GEMINI: 7, 
         const.ID_CANCER: 8, 
         const.ID_LEO: 9, 
         const.ID_VIRGO: 10, 
         const.ID_LIBRA: 11, 
         const.ID_SCORPIO: 12}
        return switcher.get(id, '?')

    def switch_asc_capricorn(self, id):
        switcher = {const.ID_CAPRICORN: 1, 
         const.ID_AQUARIUS: 2, 
         const.ID_PISCES: 3, 
         const.ID_ARIES: 4, 
         const.ID_TAURUS: 5, 
         const.ID_GEMINI: 6, 
         const.ID_CANCER: 7, 
         const.ID_LEO: 8, 
         const.ID_VIRGO: 9, 
         const.ID_LIBRA: 10, 
         const.ID_SCORPIO: 11, 
         const.ID_SAGITTARIUS: 12}
        return switcher.get(id, '?')

    def switch_asc_aquarius(self, id):
        switcher = {const.ID_AQUARIUS: 1, 
         const.ID_PISCES: 2, 
         const.ID_ARIES: 3, 
         const.ID_TAURUS: 4, 
         const.ID_GEMINI: 5, 
         const.ID_CANCER: 6, 
         const.ID_LEO: 7, 
         const.ID_VIRGO: 8, 
         const.ID_LIBRA: 9, 
         const.ID_SCORPIO: 10, 
         const.ID_SAGITTARIUS: 11, 
         const.ID_CAPRICORN: 12}
        return switcher.get(id, '?')

    def switch_asc_pisces(self, id):
        switcher = {const.ID_PISCES: 1, 
         const.ID_ARIES: 2, 
         const.ID_TAURUS: 2, 
         const.ID_GEMINI: 4, 
         const.ID_CANCER: 5, 
         const.ID_LEO: 6, 
         const.ID_VIRGO: 7, 
         const.ID_LIBRA: 8, 
         const.ID_SCORPIO: 9, 
         const.ID_SAGITTARIUS: 10, 
         const.ID_CAPRICORN: 11, 
         const.ID_AQUARIUS: 12}
        return switcher.get(id, '?')