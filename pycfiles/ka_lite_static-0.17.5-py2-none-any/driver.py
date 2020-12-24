# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/gdal/driver.py
# Compiled at: 2018-07-11 18:15:30
from ctypes import c_void_p
from django.contrib.gis.gdal.base import GDALBase
from django.contrib.gis.gdal.error import OGRException
from django.contrib.gis.gdal.prototypes import ds as capi
from django.utils import six
from django.utils.encoding import force_bytes

class Driver(GDALBase):
    """Wraps an OGR Data Source Driver."""
    _alias = {'esri': 'ESRI Shapefile', 'shp': 'ESRI Shapefile', 
       'shape': 'ESRI Shapefile', 
       'tiger': 'TIGER', 
       'tiger/line': 'TIGER'}

    def __init__(self, dr_input):
        """Initializes an OGR driver on either a string or integer input."""
        if isinstance(dr_input, six.string_types):
            self._register()
            if dr_input.lower() in self._alias:
                name = self._alias[dr_input.lower()]
            else:
                name = dr_input
            dr = capi.get_driver_by_name(force_bytes(name))
        elif isinstance(dr_input, int):
            self._register()
            dr = capi.get_driver(dr_input)
        elif isinstance(dr_input, c_void_p):
            dr = dr_input
        else:
            raise OGRException('Unrecognized input type for OGR Driver: %s' % str(type(dr_input)))
        if not dr:
            raise OGRException('Could not initialize OGR Driver on input: %s' % str(dr_input))
        self.ptr = dr

    def __str__(self):
        """Returns the string name of the OGR Driver."""
        return capi.get_driver_name(self.ptr)

    def _register(self):
        """Attempts to register all the data source drivers."""
        if not self.driver_count:
            capi.register_all()

    @property
    def driver_count(self):
        """Returns the number of OGR data source drivers registered."""
        return capi.get_driver_count()