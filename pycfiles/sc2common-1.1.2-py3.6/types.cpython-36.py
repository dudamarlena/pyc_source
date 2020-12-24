# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2common\types.py
# Compiled at: 2018-12-23 16:00:58
# Size of source mod 2**32: 5552 bytes
from s2clientprotocol import sc2api_pb2 as sc_pb
from s2clientprotocol import common_pb2 as races
from sc2common.containers import RestrictedType
from sc2common import constants as c

class PlayerControls(RestrictedType):
    __doc__ = "sc2protocol related internals used to define the agent's interface to control its units"
    ALLOWED_TYPES = {c.COMPUTER: sc_pb.Computer, 
     c.OBSERVER: sc_pb.Observer, 
     c.PARTICIPANT: sc_pb.Participant}


class PlayerDesigns(RestrictedType):
    __doc__ = 'a description of how unit controls are administered by an agent'
    ALLOWED_TYPES = [
     c.COMPUTER,
     c.HUMAN,
     c.BOT,
     c.AI,
     c.ARCHON]


class ComputerDifficulties(RestrictedType):
    __doc__ = "how difficult Blizzard's internal bot is made to be"
    ALLOWED_TYPES = {c.VERYEASY: sc_pb.VeryEasy, 
     c.EASY: sc_pb.Easy, 
     c.MEDIUM: sc_pb.Medium, 
     c.MEDIUMHARD: sc_pb.MediumHard, 
     c.HARD: sc_pb.Hard, 
     c.HARDER: sc_pb.Harder, 
     c.VERYHARD: sc_pb.VeryHard, 
     c.CHEATVISION: sc_pb.CheatVision, 
     c.CHEATMONEY: sc_pb.CheatMoney, 
     c.CHEATINSANE: sc_pb.CheatInsane, 
     None: None}


class ActualRaces(RestrictedType):
    __doc__ = 'the set of races that a player can actually be after the game begins'
    ALLOWED_TYPES = {c.PROTOSS: races.Protoss, 
     c.ZERG: races.Zerg, 
     c.TERRAN: races.Terran, 
     None: None}


class SelectRaces(ActualRaces):
    __doc__ = 'the set of races that can be selected before a game begins'
    ALLOWED_TYPES = {c.PROTOSS: races.Protoss, 
     c.ZERG: races.Zerg, 
     c.TERRAN: races.Terran, 
     c.RANDOM: races.Random}


class GameModes(RestrictedType):
    __doc__ = 'standard ways in which Starcraft2 can be played'
    ALLOWED_TYPES = [
     c.MODE_1V1]


class GameStates(RestrictedType):
    __doc__ = 'the state in which the game init/run/etc. currently is'
    ALLOWED_TYPES = [
     c.GAME_INIT,
     c.GAME_LOAD,
     c.GAME_PLAY,
     c.GAME_STOP]


class ExpansionNames(RestrictedType):
    __doc__ = 'the named expansions released by Blizzard (R)'
    ALLOWED_TYPES = [
     c.WINGS_OF_LIBERTY,
     c.HEART_OF_THE_SWARM,
     c.LEGACY_OF_THE_VOID]


class MatchResult(RestrictedType):
    __doc__ = 'the possible outcomes from a Starcraft 2 match for a player'
    ALLOWED_TYPES = {'victory':c.RESULT_VICTORY, 
     'defeat':c.RESULT_DEFEAT, 
     'tie':c.RESULT_TIE, 
     'undecided':c.RESULT_UNDECIDED, 
     'crash':c.RESULT_CRASH, 
     'disconnect':c.RESULT_DISCONNECT}


class PlayerRelations(RestrictedType):
    __doc__ = 'the possible relationships a player can have with another player'
    ALLOWED_TYPES = [
     c.RELATION_SELF,
     c.RELATION_ALLY,
     c.RELATION_NEUTRAL,
     c.RELATION_ENEMY]


class CloakStates(RestrictedType):
    __doc__ = 'the possible cloak states a unit can manifest'
    ALLOWED_TYPES = [
     c.CLOAKED,
     c.CLOAKED_DETECTED,
     c.NOT_CLOAKED]