# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/hydraulic/fluids.py
# Compiled at: 2020-01-31 09:10:08
# Size of source mod 2**32: 567 bytes
"""
Fluids database
"""
from copy import copy

class Fluid:

    def __init__(self, rho, nu, heat_capacity, name=''):
        self.rho = rho
        self.nu = nu
        self.heat_capacity = heat_capacity
        self.name = name

    def Dict(self):
        return copy(self.__dict__)

    @classmethod
    def DictToObject(cls, dict_):
        fluid = cls(dict_['rhos'], dict_['nu'], dict_['heat_capacity'], dict_['name'])
        return fluid


water = Fluid(1000, 0.0010518, 4185, 'Water')