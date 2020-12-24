# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/lists.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 2804 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)

    This module provides classes for handling lists of 
    Astrology Objects, Houses and Fixed Stars.
    
    It is basically a wrapper around a native dict with 
    useful augmentations.

"""
from . import aspects

class GenericList:
    __doc__ = ' This class represents a Generic List of Objects,\n    Houses or Fixed Stars.\n    \n    Although this class internally implements a dict object\n    internally, so that retrievals are faster, its public \n    interfaces are more like a list.\n    \n    '

    def __init__(self, values=[]):
        """ Builds a Generic List from a list of objects. """
        self.content = {}
        for obj in values:
            self.content[obj.id] = obj

    def add(self, obj):
        """ Adds an object to this list. """
        self.content[obj.id] = obj

    def get(self, ID):
        """ Retrieves an object from this list. """
        return self.content[ID]

    def copy(self):
        """ Returns a deep copy of this list. """
        values = [obj.copy() for obj in self]
        return GenericList(values)

    def __iter__(self):
        """ Returns an iterator to this list. """
        return self.content.values().__iter__()


class ObjectList(GenericList):
    __doc__ = ' Implements a list of astrology objects. '

    def getObjectsInHouse(self, house):
        """ Returns a list with all objects in a house. """
        res = [obj for obj in self if house.hasObject(obj)]
        return ObjectList(res)

    def getObjectsAspecting(self, point, aspList):
        """ Returns a list of objects aspecting a point 
        considering a list of possible aspects.
        
        """
        res = []
        for obj in self:
            if obj.isPlanet() and aspects.isAspecting(obj, point, aspList):
                res.append(obj)

        return ObjectList(res)


class HouseList(GenericList):
    __doc__ = ' Implements a list of houses. '

    def getHouseByLon(self, lon):
        """ Returns a house given a longitude. """
        for house in self:
            if house.inHouse(lon):
                return house

    def getObjectHouse(self, obj):
        """ Returns the house where an object is located. """
        return self.getHouseByLon(obj.lon)


class FixedStarList(GenericList):
    __doc__ = ' Implements a list of fixed stars. '