# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/object.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 7142 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)

    This module implements classes to represent 
    Astrology objects, such as planets, Houses 
    and Fixed-Stars.

"""
from . import const
from . import angle
from . import utils
from . import props

class GenericObject:
    __doc__ = ' This class represents a generic object and\n    includes properties which are common to all \n    objects on a chart.\n    \n    '

    def __init__(self):
        self.id = const.NO_PLANET
        self.type = const.OBJ_GENERIC
        self.lon = 0.0
        self.lat = 0.0
        self.sign = const.ARIES
        self.signlon = 0.0

    @classmethod
    def fromDict(cls, _dict):
        """ Builds instance from dictionary of properties. """
        obj = cls()
        obj.__dict__.update(_dict)
        return obj

    def copy(self):
        """ Returns a deep copy of this object. """
        return self.fromDict(self.__dict__)

    def __str__(self):
        return '<%s %s %s>' % (
         self.id,
         self.sign,
         angle.toString(self.signlon))

    def orb(self):
        """ Returns the orb of this object. """
        return -1.0

    def isPlanet(self):
        """ Returns if this object is a planet. """
        return self.type == const.OBJ_PLANET

    def eqCoords(self, zerolat=False):
        """ Returns the Equatorial Coordinates of this object. 
        Receives a boolean parameter to consider a zero latitude. 
        
        """
        lat = 0.0 if zerolat else self.lat
        return utils.eqCoords(self.lon, lat)

    def relocate(self, lon):
        """ Relocates this object to a new longitude. """
        self.lon = angle.norm(lon)
        self.signlon = self.lon % 30
        self.sign = const.LIST_SIGNS[int(self.lon / 30.0)]

    def antiscia(self):
        """ Returns antiscia object. """
        obj = self.copy()
        obj.type = const.OBJ_GENERIC
        obj.relocate(360 - obj.lon + 180)
        return obj

    def cantiscia(self):
        """ Returns contra-antiscia object. """
        obj = self.copy()
        obj.type = const.OBJ_GENERIC
        obj.relocate(360 - obj.lon)
        return obj


class Object(GenericObject):
    __doc__ = ' This class represents an Astrology object, such\n    as the sun or the moon, and includes properties and\n    functions which are common for all objects.\n    \n    '

    def __init__(self):
        super().__init__()
        self.type = const.OBJ_PLANET
        self.lonspeed = 0.0
        self.latspeed = 0.0

    def __str__(self):
        string = super().__str__()[:-1]
        return '%s %s>' % (
         string,
         angle.toString(self.lonspeed))

    def orb(self):
        """ Returns the orb of this object. """
        return props.object.orb[self.id]

    def meanMotion(self):
        """ Returns the mean daily motion of this object. """
        return props.object.meanMotion[self.id]

    def movement(self):
        """ Returns if this object is direct, retrograde 
        or stationary. 
        
        """
        if abs(self.lonspeed) < 0.0003:
            return const.STATIONARY
        if self.lonspeed > 0:
            return const.DIRECT
        return const.RETROGRADE

    def gender(self):
        """ Returns the gender of this object. """
        return props.object.gender[self.id]

    def faction(self):
        """ Returns the faction of this object. """
        return props.object.faction[self.id]

    def element(self):
        """ Returns the element of this object. """
        return props.object.element[self.id]

    def isDirect(self):
        """ Returns if this object is in direct motion. """
        return self.movement() == const.DIRECT

    def isRetrograde(self):
        """ Returns if this object is in retrograde motion. """
        return self.movement() == const.RETROGRADE

    def isStationary(self):
        """ Returns if this object is stationary. """
        return self.movement() == const.STATIONARY

    def isFast(self):
        """ Returns if this object is in fast motion. """
        return abs(self.lonspeed) >= self.meanMotion()


class House(GenericObject):
    __doc__ = ' This class represents a generic house cusp. '
    _OFFSET = -5.0

    def __init__(self):
        super().__init__()
        self.type = const.OBJ_HOUSE
        self.size = 30.0

    def __str__(self):
        string = super().__str__()[:-1]
        return '%s %s>' % (
         string,
         self.size)

    def num(self):
        """ Returns the number of this house [1..12]. """
        return int(self.id[5:])

    def condition(self):
        """ Returns the condition of this house. 
        The house can be angular, succedent or cadent.
    
        """
        return props.house.condition[self.id]

    def gender(self):
        """ Returns the gender of this house. """
        return props.house.gender[self.id]

    def isAboveHorizon(self):
        """ Returns true if this house is above horizon. """
        return self.id in props.house.aboveHorizon

    def inHouse(self, lon):
        """ Returns if a longitude belongs to this house. """
        dist = angle.distance(self.lon + House._OFFSET, lon)
        return dist < self.size

    def hasObject(self, obj):
        """ Returns true if an object is in this house. """
        return self.inHouse(obj.lon)


class FixedStar(GenericObject):
    __doc__ = ' This class represents a generic fixed star. '

    def __init__(self):
        super().__init__()
        self.type = const.OBJ_FIXED_STAR
        self.mag = 0.0

    def __str__(self):
        string = super().__str__()[:-1]
        return '%s %s>' % (
         string,
         self.mag)

    _ORBS = [
     [
      2, 7.5], [3, 5.5], [4, 3.5], [5, 1.5]]

    def orb(self):
        """ Returns the orb of this fixed star. """
        for mag, orb in FixedStar._ORBS:
            if self.mag < mag:
                return orb

        return 0.5

    def aspects(self, obj):
        """ Returns true if this star aspects another object.
        Fixed stars only aspect by conjunctions. 
        
        """
        dist = angle.closestdistance(self.lon, obj.lon)
        return abs(dist) < self.orb()