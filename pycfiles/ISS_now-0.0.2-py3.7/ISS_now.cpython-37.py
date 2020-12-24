# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\ISS\ISS_now.py
# Compiled at: 2019-07-10 23:56:44
# Size of source mod 2**32: 553 bytes
import json, urllib.request, time

def ISS_now():
    url = 'http://api.open-notify.org/iss-now.json'
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    location = result['iss_position']
    lat = location['latitude']
    lon = location['longitude']
    msg = result['message']
    timen = result['timestamp']
    print('time:', time.asctime(time.localtime(time.time())))
    print('timestamp:', timen)
    print('message:', msg)
    print('latitude:', lat)
    print('longitude:', lon)