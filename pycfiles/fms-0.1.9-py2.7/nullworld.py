# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fms/worlds/nullworld.py
# Compiled at: 2008-11-21 03:36:23
"""
A minimal and over simplistic world class
"""
from fms import worlds

class NullWorld(worlds.World):
    """
    Minimal world class
    """

    def __init__(self, parameters=None):
        worlds.World.__init__(self)

    def state(self):
        """
        Nullworld only returns last market info (dict)
        """
        return self.lastmarketinfo


if __name__ == '__main__':
    print NullWorld()