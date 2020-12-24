# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\game_hero\game_constants.py
# Compiled at: 2020-01-24 07:34:21
# Size of source mod 2**32: 613 bytes
"""
Constants used thorought the game.
"""
TOTAL_FIGHT_ROUNDS = 20
STANDARD_PLAYER_CONFIG = {'name':'InGameCharacter', 
 'health':(0, 100), 
 'strength':(0, 100), 
 'defence':(0, 100), 
 'speed':(0, 100), 
 'luck':(0, 100)}
ORDERUS_CONFIG = {'name':'Orderus', 
 'health':(70, 100), 
 'strength':(70, 80), 
 'defence':(45, 55), 
 'speed':(40, 50), 
 'luck':(10, 30)}
WILDBEAST_CONFIG = {'name':'WildBeast', 
 'health':(60, 90), 
 'strength':(60, 90), 
 'defence':(40, 60), 
 'speed':(40, 60), 
 'luck':(25, 40)}