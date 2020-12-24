# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astro_py/text/zodiac_text.py
# Compiled at: 2019-10-15 19:11:35
# Size of source mod 2**32: 2113 bytes
import astro_py.zodiac as zodiac
from flatlib import const

def FileCheck(fn):
    try:
        open(fn, 'r')
        return 1
    except IOError:
        return 0


class astro_py_text:

    def __init__(self, zodiac):
        self.zodiac = zodiac

    def text_zodiac(self):
        zodiac_text_array = []
        for i in self.zodiac:
            zt = zodiac_text(i)
            zodiac_text_array.append(zt)

        return zodiac_text_array


class zodiac_text:

    def __init__(self, zodiac):
        self.sign = zodiac.sign
        self.content = self.switch_zodiac(zodiac.id)

    def switch_zodiac(self, id):
        switcher = {const.ID_ARIES: self.text_belier(), 
         const.ID_TAURUS: self.text_autre(), 
         const.ID_GEMINI: self.text_autre(), 
         const.ID_CANCER: self.text_autre(), 
         const.ID_LEO: self.text_autre(), 
         const.ID_VIRGO: self.text_autre(), 
         const.ID_LIBRA: self.text_autre(), 
         const.ID_SCORPIO: self.text_autre(), 
         const.ID_SAGITTARIUS: self.text_autre(), 
         const.ID_CAPRICORN: self.text_autre(), 
         const.ID_AQUARIUS: self.text_autre(), 
         const.ID_PISCES: self.text_autre()}
        return switcher.get(id, '?')

    def text_belier(self):
        content = ''
        if FileCheck('assets/zodiac_01_belier.dat'):
            f = open('assets/zodiac_01_belier.dat', 'r')
            content += f.read()
            f.close()
        if FileCheck('assets/zodiac_01_belier_klea.dat'):
            f = open('assets/zodiac_01_belier_klea.dat', 'r')
            content += f.read()
            f.close()
        if FileCheck('assets/zodiac_01_belier_klea_definition.dat'):
            f = open('assets/zodiac_01_belier_klea_definition.dat', 'r')
            content += f.read()
            f.close()
        return content

    def text_autre(self):
        return ''