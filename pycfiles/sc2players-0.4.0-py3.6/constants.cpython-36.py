# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2players\constants.py
# Compiled at: 2018-06-16 09:31:18
# Size of source mod 2**32: 712 bytes
"""
constants that are applicable only to sc2players package
"""
from sc2common.constants import *
from sc2common.types import *
import os

class InvalidPlayerTypeException(Exception):
    pass


class InvalidRaceException(Exception):
    pass


class InvalidDifficultyException(Exception):
    pass


PLAYERS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataPlayers')
DEFAULT_TIME_LIMIT = 90
NO_ACTIVITY_LIMIT = 10
RECENT_MATCHES = 15
DEFAULT_RATING = 500