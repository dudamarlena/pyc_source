# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/measure.py
# Compiled at: 2018-07-11 18:15:30
"""
Distance and Area objects to allow for sensible and convienient calculation
and conversions.

Authors: Robert Coup, Justin Bronn, Riccardo Di Virgilio

Inspired by GeoPy (http://exogen.case.edu/projects/geopy/)
and Geoff Biggs' PhD work on dimensioned units for robotics.
"""
__all__ = [
 'A', 'Area', 'D', 'Distance']
from decimal import Decimal
from django.utils.functional import total_ordering
from django.utils import six
NUMERIC_TYPES = six.integer_types + (float, Decimal)
AREA_PREFIX = 'sq_'

def pretty_name(obj):
    if obj.__class__ == type:
        return obj.__name__
    return obj.__class__.__name__


@total_ordering
class MeasureBase(object):
    STANDARD_UNIT = None
    ALIAS = {}
    UNITS = {}
    LALIAS = {}

    def __init__(self, default_unit=None, **kwargs):
        value, self._default_unit = self.default_units(kwargs)
        setattr(self, self.STANDARD_UNIT, value)
        if default_unit and isinstance(default_unit, six.string_types):
            self._default_unit = default_unit

    def _get_standard(self):
        return getattr(self, self.STANDARD_UNIT)

    def _set_standard(self, value):
        setattr(self, self.STANDARD_UNIT, value)

    standard = property(_get_standard, _set_standard)

    def __getattr__(self, name):
        if name in self.UNITS:
            return self.standard / self.UNITS[name]
        raise AttributeError('Unknown unit type: %s' % name)

    def __repr__(self):
        return '%s(%s=%s)' % (pretty_name(self), self._default_unit,
         getattr(self, self._default_unit))

    def __str__(self):
        return '%s %s' % (getattr(self, self._default_unit), self._default_unit)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.standard == other.standard
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.standard < other.standard
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(default_unit=self._default_unit, **{self.STANDARD_UNIT: self.standard + other.standard})
        raise TypeError('%(class)s must be added with %(class)s' % {'class': pretty_name(self)})

    def __iadd__(self, other):
        if isinstance(other, self.__class__):
            self.standard += other.standard
            return self
        raise TypeError('%(class)s must be added with %(class)s' % {'class': pretty_name(self)})

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(default_unit=self._default_unit, **{self.STANDARD_UNIT: self.standard - other.standard})
        raise TypeError('%(class)s must be subtracted from %(class)s' % {'class': pretty_name(self)})

    def __isub__(self, other):
        if isinstance(other, self.__class__):
            self.standard -= other.standard
            return self
        raise TypeError('%(class)s must be subtracted from %(class)s' % {'class': pretty_name(self)})

    def __mul__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            return self.__class__(default_unit=self._default_unit, **{self.STANDARD_UNIT: self.standard * other})
        raise TypeError('%(class)s must be multiplied with number' % {'class': pretty_name(self)})

    def __imul__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            self.standard *= float(other)
            return self
        raise TypeError('%(class)s must be multiplied with number' % {'class': pretty_name(self)})

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return self.standard / other.standard
        if isinstance(other, NUMERIC_TYPES):
            return self.__class__(default_unit=self._default_unit, **{self.STANDARD_UNIT: self.standard / other})
        raise TypeError('%(class)s must be divided with number or %(class)s' % {'class': pretty_name(self)})

    def __div__(self, other):
        return type(self).__truediv__(self, other)

    def __itruediv__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            self.standard /= float(other)
            return self
        raise TypeError('%(class)s must be divided with number' % {'class': pretty_name(self)})

    def __idiv__(self, other):
        return type(self).__itruediv__(self, other)

    def __bool__(self):
        return bool(self.standard)

    def __nonzero__(self):
        return type(self).__bool__(self)

    def default_units(self, kwargs):
        """
        Return the unit value and the default units specified
        from the given keyword arguments dictionary.
        """
        val = 0.0
        default_unit = self.STANDARD_UNIT
        for unit, value in six.iteritems(kwargs):
            if not isinstance(value, float):
                value = float(value)
            if unit in self.UNITS:
                val += self.UNITS[unit] * value
                default_unit = unit
            elif unit in self.ALIAS:
                u = self.ALIAS[unit]
                val += self.UNITS[u] * value
                default_unit = u
            else:
                lower = unit.lower()
                if lower in self.UNITS:
                    val += self.UNITS[lower] * value
                    default_unit = lower
                elif lower in self.LALIAS:
                    u = self.LALIAS[lower]
                    val += self.UNITS[u] * value
                    default_unit = u
                else:
                    raise AttributeError('Unknown unit type: %s' % unit)

        return (
         val, default_unit)

    @classmethod
    def unit_attname(cls, unit_str):
        """
        Retrieves the unit attribute name for the given unit string.
        For example, if the given unit string is 'metre', 'm' would be returned.
        An exception is raised if an attribute cannot be found.
        """
        lower = unit_str.lower()
        if unit_str in cls.UNITS:
            return unit_str
        if lower in cls.UNITS:
            return lower
        if lower in cls.LALIAS:
            return cls.LALIAS[lower]
        raise Exception('Could not find a unit keyword associated with "%s"' % unit_str)


class Distance(MeasureBase):
    STANDARD_UNIT = 'm'
    UNITS = {'chain': 20.1168, 
       'chain_benoit': 20.116782, 
       'chain_sears': 20.1167645, 
       'british_chain_benoit': 20.1167824944, 
       'british_chain_sears': 20.1167651216, 
       'british_chain_sears_truncated': 20.116756, 
       'cm': 0.01, 
       'british_ft': 0.304799471539, 
       'british_yd': 0.914398414616, 
       'clarke_ft': 0.3047972654, 
       'clarke_link': 0.201166195164, 
       'fathom': 1.8288, 
       'ft': 0.3048, 
       'german_m': 1.0000135965, 
       'gold_coast_ft': 0.304799710181508, 
       'indian_yd': 0.914398530744, 
       'inch': 0.0254, 
       'km': 1000.0, 
       'link': 0.201168, 
       'link_benoit': 0.20116782, 
       'link_sears': 0.20116765, 
       'm': 1.0, 
       'mi': 1609.344, 
       'mm': 0.001, 
       'nm': 1852.0, 
       'nm_uk': 1853.184, 
       'rod': 5.0292, 
       'sears_yd': 0.91439841, 
       'survey_ft': 0.304800609601, 
       'um': 1e-06, 
       'yd': 0.9144}
    ALIAS = {'centimeter': 'cm', 
       'foot': 'ft', 
       'inches': 'inch', 
       'kilometer': 'km', 
       'kilometre': 'km', 
       'meter': 'm', 
       'metre': 'm', 
       'micrometer': 'um', 
       'micrometre': 'um', 
       'millimeter': 'mm', 
       'millimetre': 'mm', 
       'mile': 'mi', 
       'yard': 'yd', 
       'British chain (Benoit 1895 B)': 'british_chain_benoit', 
       'British chain (Sears 1922)': 'british_chain_sears', 
       'British chain (Sears 1922 truncated)': 'british_chain_sears_truncated', 
       'British foot (Sears 1922)': 'british_ft', 
       'British foot': 'british_ft', 
       'British yard (Sears 1922)': 'british_yd', 
       'British yard': 'british_yd', 
       "Clarke's Foot": 'clarke_ft', 
       "Clarke's link": 'clarke_link', 
       'Chain (Benoit)': 'chain_benoit', 
       'Chain (Sears)': 'chain_sears', 
       'Foot (International)': 'ft', 
       'German legal metre': 'german_m', 
       'Gold Coast foot': 'gold_coast_ft', 
       'Indian yard': 'indian_yd', 
       'Link (Benoit)': 'link_benoit', 
       'Link (Sears)': 'link_sears', 
       'Nautical Mile': 'nm', 
       'Nautical Mile (UK)': 'nm_uk', 
       'US survey foot': 'survey_ft', 
       'U.S. Foot': 'survey_ft', 
       'Yard (Indian)': 'indian_yd', 
       'Yard (Sears)': 'sears_yd'}
    LALIAS = dict([ (k.lower(), v) for k, v in ALIAS.items() ])

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Area(default_unit=(AREA_PREFIX + self._default_unit), **{AREA_PREFIX + self.STANDARD_UNIT: self.standard * other.standard})
        if isinstance(other, NUMERIC_TYPES):
            return self.__class__(default_unit=self._default_unit, **{self.STANDARD_UNIT: self.standard * other})
        raise TypeError('%(distance)s must be multiplied with number or %(distance)s' % {'distance': pretty_name(self.__class__)})


class Area(MeasureBase):
    STANDARD_UNIT = AREA_PREFIX + Distance.STANDARD_UNIT
    UNITS = dict([ ('%s%s' % (AREA_PREFIX, k), v ** 2) for k, v in Distance.UNITS.items() ])
    ALIAS = dict([ (k, '%s%s' % (AREA_PREFIX, v)) for k, v in Distance.ALIAS.items() ])
    LALIAS = dict([ (k.lower(), v) for k, v in ALIAS.items() ])

    def __truediv__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            return self.__class__(default_unit=self._default_unit, **{self.STANDARD_UNIT: self.standard / other})
        raise TypeError('%(class)s must be divided by a number' % {'class': pretty_name(self)})

    def __div__(self, other):
        return type(self).__truediv__(self, other)


D = Distance
A = Area