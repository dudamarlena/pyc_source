# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2simulator\setup\mapLocations.py
# Compiled at: 2018-10-01 22:18:26
# Size of source mod 2**32: 7058 bytes
import itertools, math, random
from sc2simulator import constants as c
mapDimensions = None

def defineLocs(locP1, locP2, d):
    """ensure both player locations are defined as map location tuples"""
    global mapDimensions
    dim = mapDimensions
    if not any([locP1, locP2]):
        locP1 = pickValidMapLoc()
        locP2 = pickBoundMapLoc(locP1, d)
    else:
        if locP1:
            locP1 = convertStrToPoint(locP1, dim)
            locP2 = pickBoundMapLoc(locP1, d)
        else:
            if locP2:
                locP2 = convertStrToPoint(locP2, dim)
                locP1 = pickBoundMapLoc(locP2, d)
            else:
                locP1 = convertStrToPoint(locP1, dim)
                locP2 = convertStrToPoint(locP2, dim)
    return (
     locP1, locP2)


def convertStrToPoint(value, dim=None):
    ret = [float(v) for v in value.split(',')]
    ret = ret[:3]
    ret += [0.0] * (3 - len(ret))
    if dim:
        if not isValidLoc(ret, dim):
            raise ValueError('provided location %s is not within %s' % (
             str(ret), str(dim)))
    return ret


def pickValidMapLoc(pad=30):
    """determine any location which is placeable on the map"""
    x, y = mapDimensions[:2]
    w = x - pad * 2
    l = y - pad * 2
    return (pad + random.random() * w,
     pad + random.random() * l,
     0.0)


def isValidLoc(loc, dimensions, pad=30):
    """whether loc is valid given map's dimensions"""
    x, y, z = loc
    maxX, maxY, maxZ = dimensions
    maxX -= pad
    maxY -= pad
    maxZ -= pad
    return x >= pad and x <= maxX and y >= pad and y <= maxY


def pickBoundMapLoc(center, radius, numAttempts=0):
    """pick a specific point 'radius' distance away from center, so long as the point remains within the map's allowed dimensions"""
    maxX, maxY, dummy = mapDimensions
    angle = 2 * math.pi * random.random()
    r = radius
    circleX, circleY, dummy = center
    x = r * math.cos(angle) + circleX
    y = r * math.sin(angle) + circleY
    newLoc = (x, y, 0.0)
    if not isValidLoc(newLoc, mapDimensions):
        if numAttempts >= c.MAX_MAP_PICK_TRIES:
            raise Exception('could not successfully pick a map location after %d attempts given r=%s c=%s' % (
             numAttempts, r, str(center)))
        else:
            numAttempts += 1
        return pickBoundMapLoc(center, r, numAttempts)
    else:
        return newLoc


def setLocation(otherUnits, techUnit, location, field):
    """determine the (valid) location for techUnit to be placed, accounting for all previously placed units"""
    if field:

        def progressiveSquares(pt, idx=1):
            """locate a point as close as possible to idx"""
            validLocs = []
            uRad = techUnit.radius
            cx, cy = pt
            minX = cx - idx
            maxX = cx + idx
            minY = cy - idx
            maxY = cy + idx
            for x in range(minX, maxX + 1):
                pt1 = (
                 x, minY, 0)
                pt2 = (x, maxY, 0)
                if field.canSet(pt1, uRad, goodVal=1):
                    validLocs.append(pt1)
                if field.canSet(pt2, uRad, goodVal=1):
                    validLocs.append(pt2)

            for y in range(minY + 1, maxY + 2):
                pt1 = (
                 minX, y, 0)
                pt2 = (maxX, y, 0)
                if field.canSet(pt1, uRad, goodVal=1):
                    validLocs.append(pt1)
                if field.canSet(pt2, uRad, goodVal=1):
                    validLocs.append(pt2)

            if validLocs:
                pick = random.choice(validLocs)
                newPt = [term / 2.0 for term in pick]
                field.setValues((pick[:2]), radius=([uRad] * 2), newVal=0, shape=(c.cs.SQUARE))
                return newPt
            else:
                return progressiveSquares(pt, idx=(idx + 1))

        if techUnit.isAir:
            return location
        else:
            halfPt = [2 * term for term in location]
            halfLoc = (c.cu.MapPoint)(*halfPt)
            halfLoc = c.cf.gridSnap(halfLoc)
            return progressiveSquares((int(halfLoc.x), int(halfLoc.y)))
    raise NotImplementedError("TODO -- assign each unit's map location")


def pickCloserLoc(location, length):
    """picks a location 'length' distance toward the center from 'location'"""
    dims = mapDimensions[:2]
    x, y = location[:2]
    if length == 0:
        return (x, y)
    else:
        xMid, yMid = [i / 2.0 for i in dims]
        theta = math.atan2(yMid - y, xMid - x)
        newX = x + math.cos(theta) * length
        newY = y + math.sin(theta) * length
        return (newX, newY)


def pickFurtherLoc(location, length):
    """picks a location 'length' distance toward the center from 'location'"""
    dims = mapDimensions[:2]
    x, y = location[:2]
    if length == 0:
        return (x, y)
    else:
        xMid, yMid = [i / 2.0 for i in dims]
        theta = math.atan2(yMid - y, xMid - x)
        newX = x - math.cos(theta) * length
        newY = y - math.sin(theta) * length
        return (newX, newY)