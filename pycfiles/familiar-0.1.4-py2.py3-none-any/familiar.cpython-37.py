# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jeffsalisbury/Documents/Code/Python_Code/familiar/familiar_tools/familiar.py
# Compiled at: 2020-03-23 14:18:13
# Size of source mod 2**32: 388 bytes
from familiar_tools.settings import api_settings

def dice_roll(number_of_dice, dice_sides, mod):
    import random
    total = 0
    for i in range(1, number_of_dice + 1):
        total += random.randint(1, dice_sides)

    return total + mod


def get_modifier(stat):
    mod = stat - 10
    mod = mod / 2
    return round(mod)


def get_game_version():
    return api_settings.VERSION