# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/projects/volunteer-coordination/volunteerhub/apps/volunteers/utils.py
# Compiled at: 2014-06-10 15:49:30
import json, urllib

def get_lat_long(location):
    location = urllib.quote_plus(location)
    request = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location
    try:
        response = urllib.urlopen(request)
    except:
        return ''

    data = json.load(response)
    try:
        coords = data['results'][0]['geometry']['location']
        return '%s, %s' % (coords['lat'], coords['lng'])
    except:
        return ''