# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/gdal/libgdal.py
# Compiled at: 2019-02-14 00:35:16
from __future__ import unicode_literals
import logging, os, re
from ctypes import CDLL, CFUNCTYPE, c_char_p, c_int
from ctypes.util import find_library
from django.contrib.gis.gdal.error import GDALException
from django.core.exceptions import ImproperlyConfigured
logger = logging.getLogger(b'django.contrib.gis')
try:
    from django.conf import settings
    lib_path = settings.GDAL_LIBRARY_PATH
except (AttributeError, EnvironmentError, ImportError, ImproperlyConfigured):
    lib_path = None

if lib_path:
    lib_names = None
elif os.name == b'nt':
    lib_names = [str(b'gdal201'), str(b'gdal20'), str(b'gdal111'), str(b'gdal110'), str(b'gdal19')]
elif os.name == b'posix':
    lib_names = [b'gdal', b'GDAL', b'gdal2.1.0', b'gdal2.0.0', b'gdal1.11.0', b'gdal1.10.0', b'gdal1.9.0']
else:
    raise ImproperlyConfigured(b'GDAL is unsupported on OS "%s".' % os.name)
if lib_names:
    for lib_name in lib_names:
        lib_path = find_library(lib_name)
        if lib_path is not None:
            break

if lib_path is None:
    raise ImproperlyConfigured(b'Could not find the GDAL library (tried "%s"). Is GDAL installed? If it is, try setting GDAL_LIBRARY_PATH in your settings.' % (b'", "').join(lib_names))
lgdal = CDLL(lib_path)
if os.name == b'nt':
    from ctypes import WinDLL
    lwingdal = WinDLL(lib_path)

def std_call(func):
    """
    Returns the correct STDCALL function for certain OSR routines on Win32
    platforms.
    """
    if os.name == b'nt':
        return lwingdal[func]
    else:
        return lgdal[func]


_version_info = std_call(b'GDALVersionInfo')
_version_info.argtypes = [c_char_p]
_version_info.restype = c_char_p

def gdal_version():
    """Returns only the GDAL version number information."""
    return _version_info(b'RELEASE_NAME')


def gdal_full_version():
    """Returns the full GDAL version information."""
    return _version_info(b'')


version_regex = re.compile(b'^(?P<major>\\d+)\\.(?P<minor>\\d+)(\\.(?P<subminor>\\d+))?')

def gdal_version_info():
    ver = gdal_version().decode()
    m = version_regex.match(ver)
    if not m:
        raise GDALException(b'Could not parse GDAL version string "%s"' % ver)
    return {key:m.group(key) for key in ('major', 'minor', 'subminor')}


_verinfo = gdal_version_info()
GDAL_MAJOR_VERSION = int(_verinfo[b'major'])
GDAL_MINOR_VERSION = int(_verinfo[b'minor'])
GDAL_SUBMINOR_VERSION = _verinfo[b'subminor'] and int(_verinfo[b'subminor'])
GDAL_VERSION = (GDAL_MAJOR_VERSION, GDAL_MINOR_VERSION, GDAL_SUBMINOR_VERSION)
del _verinfo
CPLErrorHandler = CFUNCTYPE(None, c_int, c_int, c_char_p)

def err_handler(error_class, error_number, message):
    logger.error(b'GDAL_ERROR %d: %s', error_number, message)


err_handler = CPLErrorHandler(err_handler)

def function(name, args, restype):
    func = std_call(name)
    func.argtypes = args
    func.restype = restype
    return func


set_error_handler = function(b'CPLSetErrorHandler', [CPLErrorHandler], CPLErrorHandler)
set_error_handler(err_handler)