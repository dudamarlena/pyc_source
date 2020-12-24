# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/plot/Coord.py
# Compiled at: 2017-10-03 13:07:16
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import collections
from cpip import ExceptionCpip

class ExceptionCoord(ExceptionCpip):
    """Exception class for representing Coordinates."""


class ExceptionCoordUnitConvert(ExceptionCoord):
    """Exception raised when converting units."""


BASE_UNITS = 'px'
UNIT_MAP = {None: 1.0, 
   'px': 1.0, 
   'pt': 1.0, 
   'pc': 12.0, 
   'in': 72.0, 
   'cm': 72.0 / 2.54, 
   'mm': 72.0 / 25.4}
UNIT_MAP_DEFAULT_FORMAT = {None: '%d', 
   'px': '%d', 
   'pt': '%d', 
   'pc': '%.2f', 
   'in': '%.3f', 
   'cm': '%.2f', 
   'mm': '%.1f'}
UNIT_MAP_DEFAULT_FORMAT_WITH_UNITS = {__k:UNIT_MAP_DEFAULT_FORMAT[__k] + '%s' for __k in UNIT_MAP_DEFAULT_FORMAT}

def units():
    """Returns the unsorted list of acceptable units."""
    return UNIT_MAP.keys()


def convert(val, unitFrom, unitTo):
    """Convert a value from one set of units to another."""
    if unitFrom == unitTo:
        return val
    try:
        return val * UNIT_MAP[unitFrom] / UNIT_MAP[unitTo]
    except KeyError:
        if unitFrom in UNIT_MAP:
            raise ExceptionCoordUnitConvert('Unsupported units %s' % unitTo)
        raise ExceptionCoordUnitConvert('Unsupported units %s' % unitFrom)


class Dim(collections.namedtuple('Dim', 'value units')):
    """Represents a dimension as an engineering value i.e. a number and units."""
    __slots__ = ()

    def scale(self, factor):
        """Returns a new Dim() scaled by a factor, units are unchanged."""
        return self._replace(value=self.value * factor)

    def convert(self, u):
        """Returns a new Dim() with units changed and value converted."""
        return self._replace(value=convert(self.value, self.units, u), units=u)

    def __str__(self):
        return 'Dim(%s%s)' % (self.value, self.units)

    def __add__(self, other):
        """Overload self+other, returned result has the sum of self and other.
        The units chosen are self's unless self's units are None in which case other's
        units are used (if not None)."""
        if self.units is None and other.units is not None:
            myVal = other.value + convert(self.value, self.units, other.units)
            return Dim(myVal, other.units)
        else:
            myVal = self.value + convert(other.value, other.units, self.units)
            return Dim(myVal, self.units)
            return

    def __sub__(self, other):
        """Overload self-other, returned result has the difference of self and
        other. The units chosen are self's unless self's units are None in
        which case other's units are used (if not None)."""
        if self.units is None and other.units is not None:
            myVal = convert(self.value, self.units, other.units) - other.value
            return Dim(myVal, other.units)
        else:
            myVal = self.value - convert(other.value, other.units, self.units)
            return Dim(myVal, self.units)
            return

    def __iadd__(self, other):
        """Addition in place, value of other is converted to my units and added."""
        self = self + other
        return self

    def __isub__(self, other):
        """Subtraction in place, value of other is subtracted."""
        self = self - other
        return self

    def __lt__(self, other):
        """Returns true if self value < other value after unit conversion."""
        return self.value < convert(other.value, other.units, self.units)

    def __le__(self, other):
        """Returns true if self value <= other value after unit conversion."""
        return self.value <= convert(other.value, other.units, self.units)

    def __eq__(self, other):
        """Returns true if self value == other value after unit conversion."""
        return self.value == convert(other.value, other.units, self.units)

    def __ne__(self, other):
        """Returns true if self value != other value after unit conversion."""
        return self.value != convert(other.value, other.units, self.units)

    def __gt__(self, other):
        """Returns true if self value > other value after unit conversion."""
        return self.value > convert(other.value, other.units, self.units)

    def __ge__(self, other):
        """Returns true if self value >= other value after unit conversion."""
        return self.value >= convert(other.value, other.units, self.units)


class Box(collections.namedtuple('Box', 'width depth')):
    __slots__ = ()

    def __str__(self):
        """Stringifying."""
        return 'Box(width=%s, depth=%s)' % (self.width, self.depth)


class Pad(collections.namedtuple('Pad', 'prev next parent child')):
    """Padding around another object that forms the Bounding Box.
    All 4 attributes are Dim() objects"""
    __slots__ = ()

    def __str__(self):
        """Stringifying."""
        return 'Pad(prev=%s, next=%s, parent=%s, child=%s)' % (
         self.prev, self.next, self.parent, self.child)


class Pt(collections.namedtuple('Pt', 'x y')):
    """A point, an absolute x/y position on the plot area.
    Members are Coord.Dim()."""
    __slots__ = ()

    def __eq__(self, other):
        """Comparison."""
        return self.x == other.x and self.y == other.y

    def __str__(self):
        """Stringifying."""
        return 'Pt(x=%s, y=%s)' % (
         self.x, self.y)

    def convert(self, u):
        """Returns a new Pt() with units changed and value converted."""
        return self._replace(x=self.x.convert(u), y=self.y.convert(u))

    def scale(self, factor):
        """Returns a new Pt() scaled by a factor, units are unchanged."""
        return self._replace(x=self.x.scale(factor), y=self.y.scale(factor))


def baseUnitsDim(theLen):
    """Returns a Coord.Dim() of length and units BASE_UNITS."""
    return Dim(theLen, BASE_UNITS)


def zeroBaseUnitsDim():
    """Returns a Coord.Dim() of zero length and units BASE_UNITS."""
    return baseUnitsDim(0.0)


def zeroBaseUnitsBox():
    """Returns a Coord.Box() of zero dimensions and units BASE_UNITS."""
    return Box(zeroBaseUnitsDim(), zeroBaseUnitsDim())


def zeroBaseUnitsPad():
    """Returns a Coord.Pad() of zero dimensions and units BASE_UNITS."""
    return Pad(zeroBaseUnitsDim(), zeroBaseUnitsDim(), zeroBaseUnitsDim(), zeroBaseUnitsDim())


def zeroBaseUnitsPt():
    """Returns a Coord.Dim() of zero length and units BASE_UNITS."""
    return Pt(zeroBaseUnitsDim(), zeroBaseUnitsDim())


def newPt(theP, incX=None, incY=None):
    """Returns a new Pt object by incrementing existing point incX, incY
    that are both Dim() objects or None."""
    newX = theP.x
    if incX is not None:
        newX += incX
    newY = theP.y
    if incY is not None:
        newY += incY
    return Pt(x=newX, y=newY)


def convertPt(theP, theUnits):
    """Returns a new point with the dimensions of theP converted to theUnits."""
    return Pt(x=Dim(convert(theP.x.value, theP.x.units, theUnits), theUnits), y=Dim(convert(theP.y.value, theP.y.units, theUnits), theUnits))