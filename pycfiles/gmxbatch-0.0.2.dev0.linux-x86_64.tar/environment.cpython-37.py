# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/environment/environment.py
# Compiled at: 2020-02-16 06:26:43
# Size of source mod 2**32: 276 bytes
from .barostat import Barostat
from .thermostat import Thermostat

class Environment:
    barostat: Barostat
    thermostat: Thermostat

    def __init__(self, thermostat: Thermostat, barostat: Barostat):
        self.thermostat = thermostat
        self.barostat = barostat