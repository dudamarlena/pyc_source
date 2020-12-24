# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\simulators\csvSimulator.py
# Compiled at: 2014-12-03 13:11:45
# Size of source mod 2**32: 233 bytes
from maverig.data.components.abstractComponent import Simulator

class CSVSimulator(Simulator):
    name = 'CSV'
    starter = 'python'
    address = 'maverig.utils.maverig_csv:CSV'
    params = {'sim_start': None,  'datafile': None}