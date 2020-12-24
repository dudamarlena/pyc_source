# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/geos/prototypes/io.py
# Compiled at: 2018-07-11 18:15:30
import threading
from ctypes import byref, c_char_p, c_int, c_char, c_size_t, Structure, POINTER
from django.contrib.gis import memoryview
from django.contrib.gis.geos.base import GEOSBase
from django.contrib.gis.geos.libgeos import GEOM_PTR
from django.contrib.gis.geos.prototypes.errcheck import check_geom, check_string, check_sized_string
from django.contrib.gis.geos.prototypes.geom import c_uchar_p, geos_char_p
from django.contrib.gis.geos.prototypes.threadsafe import GEOSFunc
from django.utils import six
from django.utils.encoding import force_bytes

class WKTReader_st(Structure):
    pass


class WKTWriter_st(Structure):
    pass


class WKBReader_st(Structure):
    pass


class WKBWriter_st(Structure):
    pass


WKT_READ_PTR = POINTER(WKTReader_st)
WKT_WRITE_PTR = POINTER(WKTWriter_st)
WKB_READ_PTR = POINTER(WKBReader_st)
WKB_WRITE_PTR = POINTER(WKBReader_st)
wkt_reader_create = GEOSFunc('GEOSWKTReader_create')
wkt_reader_create.restype = WKT_READ_PTR
wkt_reader_destroy = GEOSFunc('GEOSWKTReader_destroy')
wkt_reader_destroy.argtypes = [WKT_READ_PTR]
wkt_reader_read = GEOSFunc('GEOSWKTReader_read')
wkt_reader_read.argtypes = [WKT_READ_PTR, c_char_p]
wkt_reader_read.restype = GEOM_PTR
wkt_reader_read.errcheck = check_geom
wkt_writer_create = GEOSFunc('GEOSWKTWriter_create')
wkt_writer_create.restype = WKT_WRITE_PTR
wkt_writer_destroy = GEOSFunc('GEOSWKTWriter_destroy')
wkt_writer_destroy.argtypes = [WKT_WRITE_PTR]
wkt_writer_write = GEOSFunc('GEOSWKTWriter_write')
wkt_writer_write.argtypes = [WKT_WRITE_PTR, GEOM_PTR]
wkt_writer_write.restype = geos_char_p
wkt_writer_write.errcheck = check_string
wkb_reader_create = GEOSFunc('GEOSWKBReader_create')
wkb_reader_create.restype = WKB_READ_PTR
wkb_reader_destroy = GEOSFunc('GEOSWKBReader_destroy')
wkb_reader_destroy.argtypes = [WKB_READ_PTR]

def wkb_read_func(func):
    func.argtypes = [
     WKB_READ_PTR, c_char_p, c_size_t]
    func.restype = GEOM_PTR
    func.errcheck = check_geom
    return func


wkb_reader_read = wkb_read_func(GEOSFunc('GEOSWKBReader_read'))
wkb_reader_read_hex = wkb_read_func(GEOSFunc('GEOSWKBReader_readHEX'))
wkb_writer_create = GEOSFunc('GEOSWKBWriter_create')
wkb_writer_create.restype = WKB_WRITE_PTR
wkb_writer_destroy = GEOSFunc('GEOSWKBWriter_destroy')
wkb_writer_destroy.argtypes = [WKB_WRITE_PTR]

def wkb_write_func(func):
    func.argtypes = [
     WKB_WRITE_PTR, GEOM_PTR, POINTER(c_size_t)]
    func.restype = c_uchar_p
    func.errcheck = check_sized_string
    return func


wkb_writer_write = wkb_write_func(GEOSFunc('GEOSWKBWriter_write'))
wkb_writer_write_hex = wkb_write_func(GEOSFunc('GEOSWKBWriter_writeHEX'))

def wkb_writer_get(func, restype=c_int):
    func.argtypes = [WKB_WRITE_PTR]
    func.restype = restype
    return func


def wkb_writer_set(func, argtype=c_int):
    func.argtypes = [WKB_WRITE_PTR, argtype]
    return func


wkb_writer_get_byteorder = wkb_writer_get(GEOSFunc('GEOSWKBWriter_getByteOrder'))
wkb_writer_set_byteorder = wkb_writer_set(GEOSFunc('GEOSWKBWriter_setByteOrder'))
wkb_writer_get_outdim = wkb_writer_get(GEOSFunc('GEOSWKBWriter_getOutputDimension'))
wkb_writer_set_outdim = wkb_writer_set(GEOSFunc('GEOSWKBWriter_setOutputDimension'))
wkb_writer_get_include_srid = wkb_writer_get(GEOSFunc('GEOSWKBWriter_getIncludeSRID'), restype=c_char)
wkb_writer_set_include_srid = wkb_writer_set(GEOSFunc('GEOSWKBWriter_setIncludeSRID'), argtype=c_char)

class IOBase(GEOSBase):
    """Base class for GEOS I/O objects."""

    def __init__(self):
        self.ptr = self._constructor()

    def __del__(self):
        if self._ptr:
            self._destructor(self._ptr)


class _WKTReader(IOBase):
    _constructor = wkt_reader_create
    _destructor = wkt_reader_destroy
    ptr_type = WKT_READ_PTR

    def read(self, wkt):
        if not isinstance(wkt, (bytes, six.string_types)):
            raise TypeError
        return wkt_reader_read(self.ptr, force_bytes(wkt))


class _WKBReader(IOBase):
    _constructor = wkb_reader_create
    _destructor = wkb_reader_destroy
    ptr_type = WKB_READ_PTR

    def read(self, wkb):
        """Returns a _pointer_ to C GEOS Geometry object from the given WKB."""
        if isinstance(wkb, memoryview):
            wkb_s = bytes(wkb)
            return wkb_reader_read(self.ptr, wkb_s, len(wkb_s))
        if isinstance(wkb, (bytes, six.string_types)):
            return wkb_reader_read_hex(self.ptr, wkb, len(wkb))
        raise TypeError


class WKTWriter(IOBase):
    _constructor = wkt_writer_create
    _destructor = wkt_writer_destroy
    ptr_type = WKT_WRITE_PTR

    def write(self, geom):
        """Returns the WKT representation of the given geometry."""
        return wkt_writer_write(self.ptr, geom.ptr)


class WKBWriter(IOBase):
    _constructor = wkb_writer_create
    _destructor = wkb_writer_destroy
    ptr_type = WKB_WRITE_PTR

    def write(self, geom):
        """Returns the WKB representation of the given geometry."""
        return memoryview(wkb_writer_write(self.ptr, geom.ptr, byref(c_size_t())))

    def write_hex(self, geom):
        """Returns the HEXEWKB representation of the given geometry."""
        return wkb_writer_write_hex(self.ptr, geom.ptr, byref(c_size_t()))

    def _get_byteorder(self):
        return wkb_writer_get_byteorder(self.ptr)

    def _set_byteorder(self, order):
        if order not in (0, 1):
            raise ValueError('Byte order parameter must be 0 (Big Endian) or 1 (Little Endian).')
        wkb_writer_set_byteorder(self.ptr, order)

    byteorder = property(_get_byteorder, _set_byteorder)

    def _get_outdim(self):
        return wkb_writer_get_outdim(self.ptr)

    def _set_outdim(self, new_dim):
        if new_dim not in (2, 3):
            raise ValueError('WKB output dimension must be 2 or 3')
        wkb_writer_set_outdim(self.ptr, new_dim)

    outdim = property(_get_outdim, _set_outdim)

    def _get_include_srid(self):
        return bool(ord(wkb_writer_get_include_srid(self.ptr)))

    def _set_include_srid(self, include):
        if bool(include):
            flag = '\x01'
        else:
            flag = '\x00'
        wkb_writer_set_include_srid(self.ptr, flag)

    srid = property(_get_include_srid, _set_include_srid)


class ThreadLocalIO(threading.local):
    wkt_r = None
    wkt_w = None
    wkb_r = None
    wkb_w = None
    ewkb_w = None


thread_context = ThreadLocalIO()

def wkt_r():
    if not thread_context.wkt_r:
        thread_context.wkt_r = _WKTReader()
    return thread_context.wkt_r


def wkt_w():
    if not thread_context.wkt_w:
        thread_context.wkt_w = WKTWriter()
    return thread_context.wkt_w


def wkb_r():
    if not thread_context.wkb_r:
        thread_context.wkb_r = _WKBReader()
    return thread_context.wkb_r


def wkb_w(dim=2):
    if not thread_context.wkb_w:
        thread_context.wkb_w = WKBWriter()
    thread_context.wkb_w.outdim = dim
    return thread_context.wkb_w


def ewkb_w(dim=2):
    if not thread_context.ewkb_w:
        thread_context.ewkb_w = WKBWriter()
        thread_context.ewkb_w.srid = True
    thread_context.ewkb_w.outdim = dim
    return thread_context.ewkb_w