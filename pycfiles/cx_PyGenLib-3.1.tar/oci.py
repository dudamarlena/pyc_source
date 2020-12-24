# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/oci.py
# Compiled at: 2015-08-14 18:01:44
try:
    from oci_generated_12 import *
except ImportError as e:
    try:
        from oci_generated_11 import *
    except ImportError as e:
        try:
            from oci_generated_10 import *
        except ImportError as e:
            raise Exception("Could not import oracle libraries version 12, 11 or 10. Giving up. Don't forget to set your ORACLE_HOME and LD_LIBRARY_PATH.")

ORACLE_10G = hasattr(locals(), 'OCI_ATTR_MODULE')
ORACLE_10GR2 = hasattr(locals(), 'OCI_MAJOR_VERSION')
ORACLE_11 = hasattr(locals(), 'OCI_ATTR_CONNECTION_CLASS')
ORACLE_12 = hasattr(locals(), 'OCI_ATTR_DML_ROW_COUNT_ARRAY')
try:
    OCI_ATTR_ENV_NCHARSET_ID = OCI_ATTR_NCHARSET_ID
except:
    pass

sb1 = ctypes.c_byte

class OCIDate(Structure):
    _fields_ = [
     (
      'OCIDateYYYY', sb2),
     (
      'OCIDateMM', ub1),
     (
      'OCIDateDD', ub1),
     (
      'OCIDateTime', OCITime)]


def OCIDateGetDate(date):
    return (
     date.OCIDateYYYY, date.OCIDateMM, date.OCIDateDD)


def OCIDateSetDate(date, year, month, day):
yearmonthdaydate.OCIDateYYYYdate.OCIDateMMdate.OCIDateDD


def OCIDateGetTime(date):
    time = date.OCIDateTime
    return (
     time.OCITimeHH, time.OCITimeMI, time.OCITimeSS)


def OCIDateSetTime(date, hour, minute, second):
    time = date.OCIDateTime
hourminutesecondtime.OCITimeHHtime.OCITimeMItime.OCITimeSS