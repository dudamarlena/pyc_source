# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astro_py/planet.py
# Compiled at: 2019-10-17 02:44:45
# Size of source mod 2**32: 1413 bytes
from flatlibfr import const
import astro_py.position as position
from astro_py.component.my_timedelta import my_timedelta, my_timedelta_deg, my_timedelta_min

class planet:

    def __init__(self, planet, asc):
        self.id = planet.id
        self.sign = planet.sign
        self.sign_pos = str(my_timedelta(0, planet.signlon * 3600))
        pos = position(asc)
        id_by_asc = pos.switch_current_sign_to_id(planet.sign)
        self.pos_circle_360 = pos.position_circle_360_object(id_by_asc, planet.signlon)
        self.svg = 'assets/svg/planet/' + planet.id + '.svg'
        self.svg_degre = 'assets/svg/degre_min/' + str(my_timedelta_deg(0, planet.signlon * 3600)) + '.svg'
        self.svg_min = 'assets/svg/degre_min/' + str(my_timedelta_min(0, planet.signlon * 3600)) + '.svg'
        self.movement = planet.movement()
        self.sw_movement_is_retrograde = planet.isRetrograde()
        if planet.id == const.NORTH_NODE or planet.id == const.SOUTH_NODE:
            self.sw_movement_is_retrograde = False