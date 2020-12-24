# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astro_py/angle.py
# Compiled at: 2019-10-17 02:50:34
# Size of source mod 2**32: 1061 bytes
from flatlibfr import const
import astro_py.position as position
from astro_py.component.my_timedelta import my_timedelta, my_timedelta_deg, my_timedelta_min

class angle:

    def __init__(self, angle, asc):
        self.id = angle.id
        self.sign = angle.sign
        self.sign_pos = str(my_timedelta(0, angle.signlon * 3600))
        pos = position(asc)
        id_by_asc = pos.switch_current_sign_to_id(angle.sign)
        self.pos_circle_360 = pos.position_circle_360_object(id_by_asc, angle.signlon)
        if angle.id == 'Asc' or angle.id == 'MC':
            self.svg = 'assets/svg/angle/' + angle.id + '.svg'
            self.svg_degre = 'assets/svg/degre_min/' + str(my_timedelta_deg(0, angle.signlon * 3600)) + '.svg'
            self.svg_min = 'assets/svg/degre_min/' + str(my_timedelta_min(0, angle.signlon * 3600)) + '.svg'
        else:
            self.svg = ''
            self.svg_degre = ''
            self.svg_min = ''