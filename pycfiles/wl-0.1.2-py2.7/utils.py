# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\wl\utils.py
# Compiled at: 2017-11-03 07:30:02
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'd01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2017, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.0'
__date__ = b'2017-11-03'
from dateutil import tz
from dateutil.tz import tzutc

def to_utc(dt):
    dt = dt.astimezone(tzutc())
    return dt.replace(tzinfo=None)


def local_to_utc(dt):
    dt = dt.replace(tzinfo=tz.gettz(b'Europe/Vienna')).astimezone(tzutc())
    return dt.replace(tzinfo=None)


def utc_to_local(dt):
    dt = dt.replace(tzinfo=tzutc()).astimezone(tz.gettz(b'Europe/Vienna'))
    return dt.replace(tzinfo=None)