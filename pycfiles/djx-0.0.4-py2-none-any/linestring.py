# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/geos/linestring.py
# Compiled at: 2019-02-14 00:35:16
from django.contrib.gis.geos import prototypes as capi
from django.contrib.gis.geos.coordseq import GEOSCoordSeq
from django.contrib.gis.geos.error import GEOSException
from django.contrib.gis.geos.geometry import GEOSGeometry, LinearGeometryMixin
from django.contrib.gis.geos.point import Point
from django.contrib.gis.shortcuts import numpy
from django.utils.six.moves import range

class LineString(LinearGeometryMixin, GEOSGeometry):
    _init_func = capi.create_linestring
    _minlength = 2
    has_cs = True

    def __init__(self, *args, **kwargs):
        """
        Initializes on the given sequence -- may take lists, tuples, NumPy arrays
        of X,Y pairs, or Point objects.  If Point objects are used, ownership is
        _not_ transferred to the LineString object.

        Examples:
         ls = LineString((1, 1), (2, 2))
         ls = LineString([(1, 1), (2, 2)])
         ls = LineString(array([(1, 1), (2, 2)]))
         ls = LineString(Point(1, 1), Point(2, 2))
        """
        if len(args) == 1:
            coords = args[0]
        else:
            coords = args
        if not (isinstance(coords, (tuple, list)) or numpy and isinstance(coords, numpy.ndarray)):
            raise TypeError('Invalid initialization input for LineStrings.')
        srid = kwargs.get('srid')
        ncoords = len(coords)
        if not ncoords:
            super(LineString, self).__init__(self._init_func(None), srid=srid)
            return
        else:
            if ncoords < self._minlength:
                raise ValueError('%s requires at least %d points, got %s.' % (
                 self.__class__.__name__,
                 self._minlength,
                 ncoords))
            if isinstance(coords, (tuple, list)):
                ndim = None
                for coord in coords:
                    if not isinstance(coord, (tuple, list, Point)):
                        raise TypeError('Each coordinate should be a sequence (list or tuple)')
                    if ndim is None:
                        ndim = len(coord)
                        self._checkdim(ndim)
                    elif len(coord) != ndim:
                        raise TypeError('Dimension mismatch.')

                numpy_coords = False
            else:
                shape = coords.shape
                if len(shape) != 2:
                    raise TypeError('Too many dimensions.')
                self._checkdim(shape[1])
                ndim = shape[1]
                numpy_coords = True
            cs = GEOSCoordSeq(capi.create_cs(ncoords, ndim), z=bool(ndim == 3))
            for i in range(ncoords):
                if numpy_coords:
                    cs[i] = coords[i, :]
                elif isinstance(coords[i], Point):
                    cs[i] = coords[i].tuple
                else:
                    cs[i] = coords[i]

            super(LineString, self).__init__(self._init_func(cs.ptr), srid=srid)
            return

    def __iter__(self):
        """Allows iteration over this LineString."""
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        """Returns the number of points in this LineString."""
        return len(self._cs)

    def _get_single_external(self, index):
        return self._cs[index]

    _get_single_internal = _get_single_external

    def _set_list(self, length, items):
        ndim = self._cs.dims
        hasz = self._cs.hasz
        cs = GEOSCoordSeq(capi.create_cs(length, ndim), z=hasz)
        for i, c in enumerate(items):
            cs[i] = c

        ptr = self._init_func(cs.ptr)
        if ptr:
            capi.destroy_geom(self.ptr)
            self.ptr = ptr
            self._post_init(self.srid)
        else:
            raise GEOSException('Geometry resulting from slice deletion was invalid.')

    def _set_single(self, index, value):
        self._checkindex(index)
        self._cs[index] = value

    def _checkdim(self, dim):
        if dim not in (2, 3):
            raise TypeError('Dimension mismatch.')

    @property
    def tuple(self):
        """Returns a tuple version of the geometry from the coordinate sequence."""
        return self._cs.tuple

    coords = tuple

    def _listarr(self, func):
        """
        Internal routine that returns a sequence (list) corresponding with
        the given function.  Will return a numpy array if possible.
        """
        lst = [ func(i) for i in range(len(self)) ]
        if numpy:
            return numpy.array(lst)
        else:
            return lst

    @property
    def array(self):
        """Returns a numpy array for the LineString."""
        return self._listarr(self._cs.__getitem__)

    @property
    def x(self):
        """Returns a list or numpy array of the X variable."""
        return self._listarr(self._cs.getX)

    @property
    def y(self):
        """Returns a list or numpy array of the Y variable."""
        return self._listarr(self._cs.getY)

    @property
    def z(self):
        """Returns a list or numpy array of the Z variable."""
        if not self.hasz:
            return
        else:
            return self._listarr(self._cs.getZ)
            return


class LinearRing(LineString):
    _minlength = 4
    _init_func = capi.create_linearring