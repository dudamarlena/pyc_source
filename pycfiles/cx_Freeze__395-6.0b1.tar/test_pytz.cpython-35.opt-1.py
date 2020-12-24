# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\samples\pytz\test_pytz.py
# Compiled at: 2020-01-04 18:05:46
# Size of source mod 2**32: 467 bytes
__doc__ = 'sample to show the datetime in RFC1123 (timezone is required)'
import datetime, pytz
RFC1123 = '%a, %d %b %Y %H:%M:%S %z'
utc_time = datetime.datetime.utcnow()
print('UTC time:', utc_time.strftime(RFC1123))
tz1 = pytz.timezone('America/Sao_Paulo')
brz_time = tz1.fromutc(utc_time)
print('Brazil time:', brz_time.strftime(RFC1123))
tz2 = pytz.timezone('US/Eastern')
eas_time = tz2.fromutc(utc_time)
print('US Eastern time:', eas_time.strftime(RFC1123))