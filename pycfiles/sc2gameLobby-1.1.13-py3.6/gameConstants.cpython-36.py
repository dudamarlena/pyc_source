# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\gameConstants.py
# Compiled at: 2018-10-07 10:56:39
# Size of source mod 2**32: 1852 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
from sc2common.constants import *
from sc2common import types

class TimeoutExceeded(Exception):
    pass


class UnknownPlayer(Exception):
    pass


SC2_FILE_REPLAY = 'SC2Replay'
SC2_FILE_MAP = 'SC2Map'
FOLDER_LOBBY_HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER_PLAYED_VIDEO = 'playedReplays'
FOLDER_JSON = 'jsonData'
FOLDER_ACTIVE_CONFIGS = os.path.join(FOLDER_LOBBY_HERE, 'activeGames')
FOLDER_MODS = os.path.join(FOLDER_LOBBY_HERE, 'mods')
JSON_HEADERS = ['label', 'base-version', 'version', 'data-hash', 'fixed-hash', 'replay-hash']
FILE_GAME_VERSIONS = 'versions.json'
FILE_EDITOR_MOD = 'Playground.SC2Mod'
MIN_VERSION_AI_API = 55958
FOLDER_IGNORED_MAPS = ['Melee', 'mini_games', 'Test']
FOLDER_APP_SUPPORT = 'Support%s'
FILE_EDITOR_APP = 'SC2Switcher%s.exe'
SUPPORT_32_BIT_TERMS = ['', '']
SUPPORT_64_BIT_TERMS = ['64', '_x64']
MIN_REQUIRED_PLAYERS = 2
INITIAL_TIMEOUT = 120
DEFAULT_TIMEOUT = 15
DEFAULT_HOST_DELAY = 4
REPLAY_SAVE_FREQUENCY = 10
URL_BASE = 'http://%s:%s/%s/'