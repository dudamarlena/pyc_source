# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2maptool\functions.py
# Compiled at: 2018-10-07 15:24:38
# Size of source mod 2**32: 4795 bytes
from six import iteritems
import random, re
from sc2maptool.index import getIndex
from sc2maptool import constants as c

def selectMap(name=None, excludeName=False, closestMatch=True, **tags):
    """select a map by name and/or critiera"""
    matches = filterMapAttrs(**tags)
    if not matches:
        raise c.InvalidMapSelection('could not find any matching maps given criteria: %s' % tags)
    if name:
        matches = filterMapNames(name, excludeRegex=excludeName, closestMatch=closestMatch, records=matches)
    try:
        if closestMatch:
            return random.choice(matches)
        if matches:
            return matches
    except IndexError:
        pass

    raise c.InvalidMapSelection("requested map '%s', but could not locate it within %s or its subdirectories.  Submit the map to https://github.com/ttinies/sc2gameMapRepo/tree/master/sc2maptool/maps" % (
     name, c.PATH_MAP_INSTALL))


def filterMapAttrs(records=getIndex(), **tags):
    """matches available maps if their attributes match as specified"""
    if len(tags) == 0:
        return records
    else:
        ret = []
        for record in records:
            if matchRecordAttrs(record, tags):
                ret.append(record)

        return ret


def matchRecordAttrs(mapobj, attrs):
    """attempt to match given attributes against a single map object's attributes"""
    for k, v in iteritems(attrs):
        try:
            val = getattr(mapobj, k)
        except AttributeError:
            if bool(v):
                return False
            continue

        if val != v:
            return False

    return True


def filterMapNames(regexText, records=getIndex(), excludeRegex=False, closestMatch=True):
    """matches each record against regexText according to parameters
    NOTE: the code could be written more simply, but this is loop-optimized to
          scale better with a large number of map records"""
    bestScr = 99999
    regex = re.compile(regexText, flags=(re.IGNORECASE))
    ret = []
    if excludeRegex:
        if regexText and closestMatch:
            for m in list(records):
                if re.search(regex, m.name):
                    pass
                else:
                    score = len(m.name)
                    if score == bestScr:
                        bestScr = score
                        ret.append(m)
                    else:
                        if score < bestScr:
                            bestScr = score
                            ret = [m]

        else:
            for m in list(records):
                if re.search(regex, m.name):
                    pass
                else:
                    ret.append(m)

    else:
        if regexText and closestMatch:
            for m in records:
                if not re.search(regex, m.name):
                    pass
                else:
                    score = len(m.name)
                    if score == bestScr:
                        bestScr = score
                        ret.append(m)
                    else:
                        if score < bestScr:
                            bestScr = score
                            ret = [m]

        else:
            for m in records:
                if not re.search(regex, m.name):
                    pass
                else:
                    ret.append(m)

        return ret