# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2common\constants.py
# Compiled at: 2018-12-23 16:06:55
# Size of source mod 2**32: 8543 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from pathlib import Path
import platform
from s2clientprotocol import data_pb2
from s2clientprotocol import sc2api_pb2
import sc2common.containers as cn, os
PLATFORM = platform.system()
USER_HOME_DIR = str(Path.home())
PATH_SC2_DATA = {'Darwin':USER_HOME_DIR + '/Library/Application Support/Blizzard/StarCraft II/stableid.json', 
 'Windows':USER_HOME_DIR + '/Documents/StarCraft II/stableid.json'}
WINGS_OF_LIBERTY = 'Wings_Of_Liberty'
HEART_OF_THE_SWARM = 'Heart_Of_The_Swarm'
LEGACY_OF_THE_VOID = 'Legacy_Of_The_Void'
DEFAULT_EXPANSION = LEGACY_OF_THE_VOID
EXPO_SELECT = {'lotv':LEGACY_OF_THE_VOID, 
 'hots':HEART_OF_THE_SWARM, 
 'wol':WINGS_OF_LIBERTY}
VERYEASY = 'veryeasy'
EASY = 'easy'
MEDIUM = 'medium'
MEDIUMHARD = 'mediumhard'
HARD = 'hard'
HARDER = 'harder'
VERYHARD = 'veryhard'
CHEATVISION = 'cheatvision'
CHEATMONEY = 'cheatmoney'
CHEATINSANE = 'cheatinsane'
COMPUTER = 'computer'
OBSERVER = 'observer'
PARTICIPANT = 'agent'
HUMAN = 'human'
BOT = 'bot'
AI = 'ai'
ARCHON = 'archon'
PROTOSS = 'protoss'
ZERG = 'zerg'
TERRAN = 'terran'
NEUTRAL = 'neutral'
RANDOM = 'random'
RELATION_SELF = cn.MultiType('Self', 1)
RELATION_ALLY = cn.MultiType('Ally', 2)
RELATION_NEUTRAL = cn.MultiType('Neutral', 3)
RELATION_ENEMY = cn.MultiType('Enemy', 4)
SPEED_FASTER = 22.4
SPEED_FAST = 19.2
SPEED_NORMAL = 16.0
SPEED_SLOW = 12.8
SPEED_SLOWER = 9.6
SPEED_ACTUAL = SPEED_FASTER
START_RESOURCES = (50, 0)
SUPPLY_CAP = 200
RESULT_VICTORY = sc2api_pb2._RESULT.values_by_name['Victory'].number
RESULT_DEFEAT = sc2api_pb2._RESULT.values_by_name['Defeat'].number
RESULT_TIE = sc2api_pb2._RESULT.values_by_name['Tie'].number
RESULT_UNDECIDED = sc2api_pb2._RESULT.values_by_name['Undecided'].number
RESULT_CRASH = 5
RESULT_DISCONNECT = 6
LOOP_05_MIN = int(SPEED_FASTER * 300)
LOOP_04_MIN = int(SPEED_FASTER * 240)
LOOP_03_MIN = int(SPEED_FASTER * 180)
LOOP_02_MIN = int(SPEED_FASTER * 120)
LOOP_01_MIN = int(SPEED_FASTER * 60)
LOOP_45_SEC = int(SPEED_FASTER * 45)
LOOP_30_SEC = int(SPEED_FASTER * 30)
LOOP_20_SEC = int(SPEED_FASTER * 20)
LOOP_15_SEC = int(SPEED_FASTER * 15)
LOOP_10_SEC = int(SPEED_FASTER * 10)
LOOP_08_SEC = int(round(0.499 + SPEED_FASTER * 8))
LOOP_05_SEC = int(SPEED_FASTER * 5)
LOOP_03_SEC = int(round(0.499 + SPEED_FASTER * 3))
LOOP_02_SEC = int(round(0.499 + SPEED_FASTER * 2))
LOOP_01_SEC = int(round(0.499 + SPEED_FASTER))
LOOP1384_MS = int(round(0.499 + SPEED_FASTER * 1.38))
LOOP_760_MS = int(round(0.499 + SPEED_FASTER * 0.75))
LOOP_670_MS = 15
LOOP_535_MS = 12
LOOP_491_MS = 11
LOOP_446_MS = 10
LOOP_360_MS = 8
LOOP_313_MS = 7
LOOP_270_MS = 6
LOOP_225_MS = 5
LOOP_180_MS = 4
LOOP_135_MS = 3
LOOP_090_MS = 2
LOOP_045_MS = 1
NUKE = cn.MultiType('NuclearLaunchDetected', sc2api_pb2.NuclearLaunchDetected)
NYDUS = cn.MultiType('NydusWormDetected', sc2api_pb2.NydusWormDetected)
ALERT_NAMES = [NUKE, NYDUS]
YIELD_MINERAL = 5
YIELD_MINERAL_RICH = 8
YIELD_VESPENE = 4
YIELD_VESPENE_RICH = 5
MODE_1V1 = '1v1'
MODE_1V1_BOT = '1v1bot'
MODE_1VN_BOT = '1vNbot'
MODE_2V2 = '2v2'
MODE_3V3 = '3v3'
MODE_4V4 = '4v4'
MODE_NVN = 'NvN'
MODE_NVN_BOT = 'NvNbot'
MODE_FFA = 'FFA'
MODE_FFA_BOT = 'FFAbot'
MODE_UNKNOWN = 'unknown'
LOCALHOST = '127.0.0.1'
DEFAULT_SERVER_PORT = 7801
GAME_INIT = 'game_state'
GAME_LOAD = 'load'
GAME_PLAY = 'play'
GAME_STOP = 'stop'
INVULNERABLE_HEALTH = 10000
BUFF_CARRY_MINERALS = {271,
 272}
BUFF_CARRY_VESEPENE = {273,
 274,
 275}
CLOAKED = cn.MultiType('Cloaked', 1)
CLOAKED_DETECTED = cn.MultiType('CloakedDetected', 2)
NOT_CLOAKED = cn.MultiType('NotCloaked', 3)
SC2_BANK_EXT = 'SC2Bank'
SC2_MAP_EXT = 'SC2Map'
SC2_MOD_EXT = 'SC2Mod'
SC2_REPLAY_EXT = 'SC2Replay'
PATH_NEW_MATCH_DATA = '.'