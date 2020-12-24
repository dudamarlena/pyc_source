# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\astrolib\coords\jdnow.py
# Compiled at: 2014-01-13 11:58:06
""" Simple script used to test astrodate.utc2jd function
against TPM utc_now function. Use together with jdnow.c."""
from astrodate import utc2jd
import datetime
stamp = datetime.datetime.utcnow()
print 'Now (GM) = ', stamp
print 'Now (UTC JD): %f' % utc2jd(stamp)