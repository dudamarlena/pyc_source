# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2ladderMgmt\functions.py
# Compiled at: 2018-06-02 13:28:12
# Size of source mod 2**32: 2255 bytes
"""
PURPOSE: manage records of all known ladders, both local and remote
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import glob, os, re
from sc2ladderMgmt import constants as c
from sc2ladderMgmt.ladders import ladderCache, Ladder

def addLadder(settings):
    """define a new Ladder setting and save to disk file"""
    ladder = Ladder(settings)
    ladder.save()
    getKnownLadders()[ladder.name] = ladder
    return ladder


def getLadder(name):
    """obtain a specific ladder settings file"""
    try:
        return getKnownLadders()[name.lower()]
    except KeyError:
        raise ValueError("given ladder name '%s' is not a known configuration" % name)


def delLadder(name):
    """forget about a previously defined Ladder setting by deleting its disk file"""
    ladders = getKnownLadders()
    try:
        ladder = ladders[name]
        os.remove(ladder.filename)
        del ladders[name]
        return ladder
    except KeyError:
        raise ValueError("given ladder name '%s' is not a known ladder definition" % name)


def getKnownLadders(reset=False):
    """identify all of the currently defined ladders"""
    if not ladderCache or reset:
        jsonFiles = os.path.join(c.LADDER_FOLDER, '*.json')
        for ladderFilepath in glob.glob(jsonFiles):
            filename = os.path.basename(ladderFilepath)
            name = re.search('^ladder_(.*?).json$', filename).groups()[0]
            ladder = Ladder(name)
            ladderCache[ladder.name] = ladder

    return ladderCache


__all__ = [
 'addLadder', 'getLadder', 'delLadder', 'getKnownLadders']