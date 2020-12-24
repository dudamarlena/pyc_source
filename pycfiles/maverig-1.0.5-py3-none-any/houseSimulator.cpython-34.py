# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\simulators\houseSimulator.py
# Compiled at: 2014-10-21 14:50:33
# Size of source mod 2**32: 258 bytes
from maverig.data.components.abstractComponent import Simulator

class HouseSimulator(Simulator):
    name = 'HouseSim'
    starter = 'python'
    address = 'maverig.data.components.utils.houseSim:HouseSim'
    params = {'sim_start': None,  'datafile': None}