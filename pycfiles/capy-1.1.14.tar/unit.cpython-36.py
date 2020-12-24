# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/christian/documented/ctf/ctf/unit.py
# Compiled at: 2020-03-20 19:03:03
# Size of source mod 2**32: 189 bytes


class Unit(object):

    def __init__(self, team, position, has_flag=False):
        self.team = team
        self.position = position
        self.has_flag = has_flag
        self.jail = 0