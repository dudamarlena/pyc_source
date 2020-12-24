# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\pytz\test_pytz.py
# Compiled at: 2020-01-04 18:05:46
# Size of source mod 2**32: 467 bytes
"""sample to show the datetime in RFC1123 (timezone is required)"""
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