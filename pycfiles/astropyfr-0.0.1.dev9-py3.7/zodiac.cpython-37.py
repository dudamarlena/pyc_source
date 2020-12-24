# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astro_py/zodiac.py
# Compiled at: 2019-10-17 02:44:52
# Size of source mod 2**32: 1661 bytes
from flatlibfr import const
import astro_py.position as position

class zodiac:
    __doc__ = ' This class represents the zodiac '

    def __init__(self, id, sign, asc):
        """ Creates an zodiac class """
        self.id = id
        self.sign = sign
        self.symbol = self.switch_symbol(sign)
        self.element = self.switch_element(sign)
        self.svg = 'assets/svg/zodiac/' + sign + '.svg'
        pos = position(asc)
        self.id_by_asc = pos.switch_asc(id)
        self.pos_circle_360 = pos.position_circle_360_zodiac(id)

    def switch_symbol(self, sign):
        """ Font icon of the sign """
        switcher = {const.ARIES: '♈', 
         const.TAURUS: '♉', 
         const.GEMINI: '♊', 
         const.CANCER: '♋', 
         const.LEO: '♌', 
         const.VIRGO: '♍', 
         const.LIBRA: '♎', 
         const.SCORPIO: '♏', 
         const.SAGITTARIUS: '♐', 
         const.CAPRICORN: '♑', 
         const.AQUARIUS: '♒', 
         const.PISCES: '♑'}
        return switcher.get(sign, '?')

    def switch_element(self, sign):
        """ Element of zodiac """
        switcher = {const.ARIES: 'Feu', 
         const.TAURUS: 'Terre', 
         const.GEMINI: 'Air', 
         const.CANCER: 'Eau', 
         const.LEO: 'Feu', 
         const.VIRGO: 'Terre', 
         const.LIBRA: 'Air', 
         const.SCORPIO: 'Eau', 
         const.SAGITTARIUS: 'Feu', 
         const.CAPRICORN: 'Terre', 
         const.AQUARIUS: 'Air', 
         const.PISCES: 'Eau'}
        return switcher.get(sign, '?')