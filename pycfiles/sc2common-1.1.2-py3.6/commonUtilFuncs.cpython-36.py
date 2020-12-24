# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2common\commonUtilFuncs.py
# Compiled at: 2018-12-22 13:53:33
# Size of source mod 2**32: 7651 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from s2clientprotocol import common_pb2
from sc2common.containers import MapPoint, RestrictedType
from sc2common import constants as c
import math, os, re

def determineRace(value):
    if isinstance(value, RestrictedType):
        return value.type
    if isinstance(value, int):
        if value == common_pb2.Terran:
            return c.PROTOSS
        else:
            if value == common_pb2.Zerg:
                return c.TERRAN
            if value == common_pb2.Protoss:
                return c.ZERG
        if value == common_pb2.Random:
            return c.RANDOM
    else:
        if isinstance(value, str):
            if re.search('^prot', value, flags=(re.IGNORECASE)):
                return c.PROTOSS
            else:
                if re.search('^terr', value, flags=(re.IGNORECASE)):
                    return c.TERRAN
                if re.search('^zerg', value, flags=(re.IGNORECASE)):
                    return c.ZERG
            if re.search('^rand', value, flags=(re.IGNORECASE)):
                return c.RANDOM
    raise ValueError("could not determine how to convert '%s' into a race value" % value)


def isPlayerSelf(playerValue):
    return playerValue == c.RELATION_SELF


def isPlayerAlly(playerValue):
    return playerValue == c.RELATION_ALLY


def isPlayerNeutral(playerValue):
    return playerValue == c.RELATION_NEUTRAL


def isPlayerEnemy(playerValue):
    return playerValue == c.RELATION_ENEMY


def getName(target):
    ret = target
    while True:
        try:
            ret = ret.name
        except AttributeError:
            break

    return str(ret)


def relateObjectLocs(obj, entities, selectF):
    """calculate the minimum distance to reach any iterable of entities with a loc"""
    try:
        obj = obj.loc
    except AttributeError:
        pass

    try:
        func = obj.direct2dDistance
    except AttributeError:
        raise ValueError('object %s (%s) does not possess and is not a %s' % (obj, type(obj), MapPoint))

    try:
        return selectF([(func(b.loc), b) for b in entities])
    except AttributeError:
        return selectF([(func(b), b) for b in entities])


def minDistance(obj, entities):
    return relateObjectLocs(obj, entities, min)


def maxDistance(obj, entities):
    return relateObjectLocs(obj, entities, max)


def convertToMapPoint(loc):
    if type(loc) in [list, tuple]:
        if len(loc) == 2:
            return MapPoint(loc[0], loc[1])
    if hasattr(loc, 'x'):
        if hasattr(loc, 'y'):
            return MapPoint(loc.x, loc.y)
    raise ValueError('passed location type %s which is invalid.  Given value: %s' % (type(loc), loc))


def gridSnap(point, grid=1.0):
    """cause the given point to snap to nearest X/Y grid point"""

    def snapFunc(value):
        value += 1e-06
        remainder = value % grid
        value -= remainder
        newAdd = round(remainder / grid) * grid
        return value + newAdd

    return MapPoint(snapFunc(point.x), snapFunc(point.y))


def convertToMapPic(byteString, mapWidth):
    """convert a bytestring into a 2D row x column array, representing an existing map of fog-of-war, creep, etc."""
    data = []
    line = ''
    for idx, char in enumerate(byteString):
        line += str(ord(char))
        if (idx + 1) % mapWidth == 0:
            data.append(line)
            line = ''

    return data


def Dumper(obj, indent=0, increase=4, encoding='utf-8'):
    """appropriately view a given dict/list/tuple/object data structure"""

    def p(given):
        if isinstance(given, str):
            return given.encode(encoding)
        else:
            return given

    try:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if hasattr(v, '__iter__'):
                    print('%s%s' % (' ' * indent, p(k)))
                    Dumper(v, indent=(indent + increase), increase=increase)
                else:
                    print('%s%s=%s' % (' ' * indent, p(k), p(v)))

        else:
            if isinstance(obj, list):
                for o in obj:
                    Dumper(o, indent=indent, increase=increase)

            else:
                if isinstance(obj, tuple):
                    print('%s%s' % (' ' * indent, p(obj[0])))
                    next = list(obj)[1:]
                    if len(next) == 1:
                        next = next[0]
                    else:
                        next = tuple(next)
                    Dumper(next, indent=(indent + increase), increase=increase)
                else:
                    if isinstance(obj, str):
                        print('%s%s' % (' ' * indent, p(obj)))
                    else:
                        if obj != None:
                            print('%s%s' % (' ' * indent, p(obj)))
    except Exception:
        print(type(obj), obj)


def convertSecondsToLoops(value, gamespeed=c.SPEED_NORMAL):
    conversionFactor = gamespeed
    return int(round(value * conversionFactor + 0.1))


def quadraticEval(a, b, c, x):
    """given all params return the result of quadratic equation a*x^2 + b*x + c"""
    return a * x ** 2 + b * x + c


def quadraticSolver(a, b, c):
    """return solution(s) for x, to the quadratic equation a*x^2 + b*x + c
    when it equals zero using the quadratic formula"""
    if a == 0:
        if b == 0:
            return []
        else:
            return [
             -c / float(b)]
    else:
        d = b ** 2.0 - 4 * a * c
        if d < 0:
            return []
        else:
            solvedPart0 = 1 / (2.0 * a)
            solvedPart1 = -b * solvedPart0
            if d == 0:
                return [
                 solvedPart1]
            solvedPart2 = math.sqrt(d) * solvedPart0
            return [solvedPart1 + solvedPart2, solvedPart1 - solvedPart2]