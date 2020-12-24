# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/colors.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import hashlib, colorsys

def get_hashed_color(string, l=0.5, s=0.5):
    val = int(hashlib.md5(string.encode('utf-8')).hexdigest()[:3], 16)
    tup = colorsys.hls_to_rgb(val / 4096.0, l, s)
    return '#%02x%02x%02x' % (int(tup[0] * 255), int(tup[1] * 255), int(tup[2] * 255))