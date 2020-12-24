# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/urltojson/me.py
# Compiled at: 2019-06-22 12:50:53
# Size of source mod 2**32: 108 bytes
import urllib.request, json

def get(url):
    return json.loads(urllib.request.urlopen(url).read().decode())