# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/documented/ctf/ctf/unit.py
# Compiled at: 2020-03-20 19:03:03
# Size of source mod 2**32: 189 bytes


class Unit(object):

    def __init__(self, team, position, has_flag=False):
        self.team = team
        self.position = position
        self.has_flag = has_flag
        self.jail = 0