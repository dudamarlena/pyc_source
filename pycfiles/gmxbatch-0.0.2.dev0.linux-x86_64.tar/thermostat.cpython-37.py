# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/environment/thermostat.py
# Compiled at: 2020-02-14 07:23:59
# Size of source mod 2**32: 379 bytes
from typing import List

class Thermostat:
    ref_temperature: float
    groups: List[str]
    tau: float
    algorithm = 'V-rescale'
    algorithm: str

    def __init__(self, groups: List[str], ref_temperature: float, tau: float, algorithm: str='V-rescale'):
        self.groups = groups
        self.tau = tau
        self.ref_temperature = ref_temperature
        self.algorithm = algorithm