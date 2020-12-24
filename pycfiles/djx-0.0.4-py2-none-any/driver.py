# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/gdal/driver.py
# Compiled at: 2019-02-14 00:35:16
from ctypes import c_void_p
from django.contrib.gis.gdal.base import GDALBase
from django.contrib.gis.gdal.error import GDALException
from django.contrib.gis.gdal.prototypes import ds as vcapi, raster as rcapi
from django.utils import six
from django.utils.encoding import force_bytes, force_text

class Driver(GDALBase):
    """
    Wraps a GDAL/OGR Data Source Driver.
    For more information, see the C API source code:
    http://www.gdal.org/gdal_8h.html - http://www.gdal.org/ogr__api_8h.html
    """
    _alias = {'esri': 'ESRI Shapefile', 
       'shp': 'ESRI Shapefile', 
       'shape': 'ESRI Shapefile', 
       'tiger': 'TIGER', 
       'tiger/line': 'TIGER', 
       'tiff': 'GTiff', 
       'tif': 'GTiff', 
       'jpeg': 'JPEG', 
       'jpg': 'JPEG'}

    def __init__(self, dr_input):
        """
        Initializes an GDAL/OGR driver on either a string or integer input.
        """
        if isinstance(dr_input, six.string_types):
            self.ensure_registered()
            if dr_input.lower() in self._alias:
                name = self._alias[dr_input.lower()]
            else:
                name = dr_input
            for iface in (vcapi, rcapi):
                driver = c_void_p(iface.get_driver_by_name(force_bytes(name)))
                if driver:
                    break

        elif isinstance(dr_input, int):
            self.ensure_registered()
            for iface in (vcapi, rcapi):
                driver = iface.get_driver(dr_input)
                if driver:
                    break

        elif isinstance(dr_input, c_void_p):
            driver = dr_input
        else:
            raise GDALException('Unrecognized input type for GDAL/OGR Driver: %s' % str(type(dr_input)))
        if not driver:
            raise GDALException('Could not initialize GDAL/OGR Driver on input: %s' % str(dr_input))
        self.ptr = driver

    def __str__(self):
        return self.name

    @classmethod
    def ensure_registered(cls):
        """
        Attempts to register all the data source drivers.
        """
        if not vcapi.get_driver_count():
            vcapi.register_all()
        if not rcapi.get_driver_count():
            rcapi.register_all()

    @classmethod
    def driver_count(cls):
        """
        Returns the number of GDAL/OGR data source drivers registered.
        """
        return vcapi.get_driver_count() + rcapi.get_driver_count()

    @property
    def name(self):
        """
        Returns description/name string for this driver.
        """
        return force_text(rcapi.get_driver_description(self.ptr))