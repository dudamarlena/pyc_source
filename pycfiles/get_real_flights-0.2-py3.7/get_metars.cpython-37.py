# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\src\get_metars.py
# Compiled at: 2019-02-03 20:53:18
# Size of source mod 2**32: 219 bytes
from collections import defaultdict
import requests

def get_metar(icao):
    resp = requests.get('/'.join(['https://avwx.rest/api/metar', icao]))
    metar = resp.json()
    return metar