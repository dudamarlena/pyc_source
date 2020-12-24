# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/geos/libgeos.py
# Compiled at: 2019-02-14 00:35:16
"""
 This module houses the ctypes initialization procedures, as well
 as the notice and error handler function callbacks (get called
 when an error occurs in GEOS).

 This module also houses GEOS Pointer utilities, including
 get_pointer_arr(), and GEOM_PTR.
"""
import logging, os, re
from ctypes import CDLL, CFUNCTYPE, POINTER, Structure, c_char_p
from ctypes.util import find_library
from django.contrib.gis.geos.error import GEOSException
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject
logger = logging.getLogger('django.contrib.gis')

def load_geos():
    try:
        from django.conf import settings
        lib_path = settings.GEOS_LIBRARY_PATH
    except (AttributeError, EnvironmentError, ImportError, ImproperlyConfigured):
        lib_path = None

    if lib_path:
        lib_names = None
    elif os.name == 'nt':
        lib_names = ['geos_c', 'libgeos_c-1']
    elif os.name == 'posix':
        lib_names = ['geos_c', 'GEOS']
    else:
        raise ImportError('Unsupported OS "%s"' % os.name)
    if lib_names:
        for lib_name in lib_names:
            lib_path = find_library(lib_name)
            if lib_path is not None:
                break

    if lib_path is None:
        raise ImportError('Could not find the GEOS library (tried "%s"). Try setting GEOS_LIBRARY_PATH in your settings.' % ('", "').join(lib_names))
    _lgeos = CDLL(lib_path)
    _lgeos.initGEOS_r.restype = CONTEXT_PTR
    _lgeos.finishGEOS_r.argtypes = [CONTEXT_PTR]
    return _lgeos


NOTICEFUNC = CFUNCTYPE(None, c_char_p, c_char_p)

def notice_h(fmt, lst):
    fmt, lst = fmt.decode(), lst.decode()
    try:
        warn_msg = fmt % lst
    except TypeError:
        warn_msg = fmt

    logger.warning('GEOS_NOTICE: %s\n', warn_msg)


notice_h = NOTICEFUNC(notice_h)
ERRORFUNC = CFUNCTYPE(None, c_char_p, c_char_p)

def error_h(fmt, lst):
    fmt, lst = fmt.decode(), lst.decode()
    try:
        err_msg = fmt % lst
    except TypeError:
        err_msg = fmt

    logger.error('GEOS_ERROR: %s\n', err_msg)


error_h = ERRORFUNC(error_h)

class GEOSGeom_t(Structure):
    pass


class GEOSPrepGeom_t(Structure):
    pass


class GEOSCoordSeq_t(Structure):
    pass


class GEOSContextHandle_t(Structure):
    pass


GEOM_PTR = POINTER(GEOSGeom_t)
PREPGEOM_PTR = POINTER(GEOSPrepGeom_t)
CS_PTR = POINTER(GEOSCoordSeq_t)
CONTEXT_PTR = POINTER(GEOSContextHandle_t)

def get_pointer_arr(n):
    """Gets a ctypes pointer array (of length `n`) for GEOSGeom_t opaque pointer."""
    GeomArr = GEOM_PTR * n
    return GeomArr()


lgeos = SimpleLazyObject(load_geos)

class GEOSFuncFactory(object):
    """
    Lazy loading of GEOS functions.
    """
    argtypes = None
    restype = None
    errcheck = None

    def __init__(self, func_name, *args, **kwargs):
        self.func_name = func_name
        self.restype = kwargs.pop('restype', self.restype)
        self.errcheck = kwargs.pop('errcheck', self.errcheck)
        self.argtypes = kwargs.pop('argtypes', self.argtypes)
        self.args = args
        self.kwargs = kwargs
        self.func = None
        return

    def __call__(self, *args, **kwargs):
        if self.func is None:
            self.func = self.get_func(*self.args, **self.kwargs)
        return self.func(*args, **kwargs)

    def get_func(self, *args, **kwargs):
        from django.contrib.gis.geos.prototypes.threadsafe import GEOSFunc
        func = GEOSFunc(self.func_name)
        func.argtypes = self.argtypes or []
        func.restype = self.restype
        if self.errcheck:
            func.errcheck = self.errcheck
        return func


geos_version = GEOSFuncFactory('GEOSversion', restype=c_char_p)
version_regex = re.compile('^(?P<version>(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<subminor>\\d+))((rc(?P<release_candidate>\\d+))|dev)?-CAPI-(?P<capi_version>\\d+\\.\\d+\\.\\d+)( r\\d+)?( \\w+)?$')

def geos_version_info():
    """
    Returns a dictionary containing the various version metadata parsed from
    the GEOS version string, including the version number, whether the version
    is a release candidate (and what number release candidate), and the C API
    version.
    """
    ver = geos_version().decode()
    m = version_regex.match(ver)
    if not m:
        raise GEOSException('Could not parse version info string "%s"' % ver)
    return {key:m.group(key) for key in ('version', 'release_candidate', 'capi_version',
                                         'major', 'minor', 'subminor')}