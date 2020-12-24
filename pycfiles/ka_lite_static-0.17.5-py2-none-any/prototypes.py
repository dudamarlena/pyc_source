# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/geoip/prototypes.py
# Compiled at: 2018-07-11 18:15:30
from ctypes import c_char_p, c_float, c_int, string_at, Structure, POINTER
from django.contrib.gis.geoip.libgeoip import lgeoip, free

class GeoIPRecord(Structure):
    _fields_ = [
     (
      'country_code', c_char_p),
     (
      'country_code3', c_char_p),
     (
      'country_name', c_char_p),
     (
      'region', c_char_p),
     (
      'city', c_char_p),
     (
      'postal_code', c_char_p),
     (
      'latitude', c_float),
     (
      'longitude', c_float),
     (
      'dma_code', c_int),
     (
      'area_code', c_int),
     (
      'charset', c_int),
     (
      'continent_code', c_char_p)]


geoip_char_fields = [ name for name, ctype in GeoIPRecord._fields_ if ctype is c_char_p ]
geoip_encodings = {0: 'iso-8859-1', 1: 'utf8'}

class GeoIPTag(Structure):
    pass


RECTYPE = POINTER(GeoIPRecord)
DBTYPE = POINTER(GeoIPTag)
if hasattr(lgeoip, 'GeoIP_lib_version'):
    GeoIP_lib_version = lgeoip.GeoIP_lib_version
    GeoIP_lib_version.argtypes = None
    GeoIP_lib_version.restype = c_char_p
else:
    GeoIP_lib_version = None
GeoIPRecord_delete = lgeoip.GeoIPRecord_delete
GeoIPRecord_delete.argtypes = [RECTYPE]
GeoIPRecord_delete.restype = None

def check_record(result, func, cargs):
    if bool(result):
        rec = result.contents
        record = dict((fld, getattr(rec, fld)) for fld, ctype in rec._fields_)
        encoding = geoip_encodings[record['charset']]
        for char_field in geoip_char_fields:
            if record[char_field]:
                record[char_field] = record[char_field].decode(encoding)

        GeoIPRecord_delete(result)
        return record
    else:
        return
        return


def record_output(func):
    func.argtypes = [
     DBTYPE, c_char_p]
    func.restype = RECTYPE
    func.errcheck = check_record
    return func


GeoIP_record_by_addr = record_output(lgeoip.GeoIP_record_by_addr)
GeoIP_record_by_name = record_output(lgeoip.GeoIP_record_by_name)
GeoIP_open = lgeoip.GeoIP_open
GeoIP_open.restype = DBTYPE
GeoIP_delete = lgeoip.GeoIP_delete
GeoIP_delete.argtypes = [DBTYPE]
GeoIP_delete.restype = None

class geoip_char_p(c_char_p):
    pass


def check_string(result, func, cargs):
    if result:
        s = string_at(result)
        free(result)
    else:
        s = ''
    return s


GeoIP_database_info = lgeoip.GeoIP_database_info
GeoIP_database_info.restype = geoip_char_p
GeoIP_database_info.errcheck = check_string

def string_output(func):
    func.restype = c_char_p
    return func


GeoIP_country_code_by_addr = string_output(lgeoip.GeoIP_country_code_by_addr)
GeoIP_country_code_by_name = string_output(lgeoip.GeoIP_country_code_by_name)
GeoIP_country_name_by_addr = string_output(lgeoip.GeoIP_country_name_by_addr)
GeoIP_country_name_by_name = string_output(lgeoip.GeoIP_country_name_by_name)