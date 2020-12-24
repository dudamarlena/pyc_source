# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stanley/PycharmProjects/horizon-python-client/src/mf_horizon_client/client/warnings.py
# Compiled at: 2020-03-26 22:31:55
# Size of source mod 2**32: 167 bytes
from enum import Enum

class Warnings(Enum):
    NO_MAX_FIRE_AND_FORGET_WORKERS_SPECIFIED = 'No maximum number of concurrent pipelines specified. Defaulting to one.'