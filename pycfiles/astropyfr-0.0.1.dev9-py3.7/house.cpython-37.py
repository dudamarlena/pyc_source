# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astro_py/house.py
# Compiled at: 2019-10-17 02:44:42
# Size of source mod 2**32: 1189 bytes
from flatlibfr import const
import astro_py.position as position
import astro_py.component.my_timedelta as my_timedelta

class house:

    def __init__(self, house, asc):
        self.id = self.switch_house(house_id=(house.id))
        self.sign = house.sign
        self.sign_pos = str(my_timedelta(0, house.signlon * 3600))
        pos = position(asc)
        id_by_asc = pos.switch_current_sign_to_id(house.sign)
        self.pos_circle_360 = pos.position_circle_360_object(id_by_asc, house.signlon)
        self.svg = 'assets/svg/house/' + str(self.id) + '.svg'

    def switch_house(self, house_id):
        """ Switch case for give the id of house """
        switcher = {const.HOUSE1: 1, 
         const.HOUSE2: 2, 
         const.HOUSE3: 3, 
         const.HOUSE4: 4, 
         const.HOUSE5: 5, 
         const.HOUSE6: 6, 
         const.HOUSE7: 7, 
         const.HOUSE8: 8, 
         const.HOUSE9: 9, 
         const.HOUSE10: 10, 
         const.HOUSE11: 11, 
         const.HOUSE12: 12}
        return switcher.get(house_id, '?')