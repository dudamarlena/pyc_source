# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/geos/point.py
# Compiled at: 2018-07-11 18:15:30
from ctypes import c_uint
from django.contrib.gis.geos.error import GEOSException
from django.contrib.gis.geos.geometry import GEOSGeometry
from django.contrib.gis.geos import prototypes as capi
from django.utils import six
from django.utils.six.moves import xrange

class Point(GEOSGeometry):
    _minlength = 2
    _maxlength = 3

    def __init__(self, x, y=None, z=None, srid=None):
        """
        The Point object may be initialized with either a tuple, or individual
        parameters.

        For Example:
        >>> p = Point((5, 23)) # 2D point, passed in as a tuple
        >>> p = Point(5, 23, 8) # 3D point, passed in with individual parameters
        """
        if isinstance(x, (tuple, list)):
            ndim = len(x)
            coords = x
        elif isinstance(x, six.integer_types + (float,)) and isinstance(y, six.integer_types + (float,)):
            if isinstance(z, six.integer_types + (float,)):
                ndim = 3
                coords = [x, y, z]
            else:
                ndim = 2
                coords = [x, y]
        else:
            raise TypeError('Invalid parameters given for Point initialization.')
        point = self._create_point(ndim, coords)
        super(Point, self).__init__(point, srid=srid)

    def _create_point(self, ndim, coords):
        """
        Create a coordinate sequence, set X, Y, [Z], and create point
        """
        if ndim < 2 or ndim > 3:
            raise TypeError('Invalid point dimension: %s' % str(ndim))
        cs = capi.create_cs(c_uint(1), c_uint(ndim))
        i = iter(coords)
        capi.cs_setx(cs, 0, next(i))
        capi.cs_sety(cs, 0, next(i))
        if ndim == 3:
            capi.cs_setz(cs, 0, next(i))
        return capi.create_point(cs)

    def _set_list(self, length, items):
        ptr = self._create_point(length, items)
        if ptr:
            capi.destroy_geom(self.ptr)
            self._ptr = ptr
            self._set_cs()
        else:
            raise GEOSException('Geometry resulting from slice deletion was invalid.')

    def _set_single(self, index, value):
        self._cs.setOrdinate(index, 0, value)

    def __iter__(self):
        """Allows iteration over coordinates of this Point."""
        for i in xrange(len(self)):
            yield self[i]

    def __len__(self):
        """Returns the number of dimensions for this Point (either 0, 2 or 3)."""
        if self.empty:
            return 0
        else:
            if self.hasz:
                return 3
            return 2

    def _get_single_external(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            return self.z

    _get_single_internal = _get_single_external

    def get_x(self):
        """Returns the X component of the Point."""
        return self._cs.getOrdinate(0, 0)

    def set_x(self, value):
        """Sets the X component of the Point."""
        self._cs.setOrdinate(0, 0, value)

    def get_y(self):
        """Returns the Y component of the Point."""
        return self._cs.getOrdinate(1, 0)

    def set_y(self, value):
        """Sets the Y component of the Point."""
        self._cs.setOrdinate(1, 0, value)

    def get_z(self):
        """Returns the Z component of the Point."""
        if self.hasz:
            return self._cs.getOrdinate(2, 0)
        else:
            return
            return

    def set_z(self, value):
        """Sets the Z component of the Point."""
        if self.hasz:
            self._cs.setOrdinate(2, 0, value)
        else:
            raise GEOSException('Cannot set Z on 2D Point.')

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)

    def get_coords(self):
        """Returns a tuple of the point."""
        return self._cs.tuple

    def set_coords(self, tup):
        """Sets the coordinates of the point with the given tuple."""
        self._cs[0] = tup

    tuple = property(get_coords, set_coords)
    coords = tuple