# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/Datos/devel/hg-repos/scru/scru/imgur.py
# Compiled at: 2011-06-05 20:38:04
import base64, json, urllib, urllib2
IMGUR_UPLOAD_URL = 'http://api.imgur.com/2/upload.json'
API_KEY = '60bbfaa8c24ff3428c4591ed252523ff'

class ApiKeyNotSpecified(Exception):
    """'No API key is specified"""
    pass


def upload(image, api_key=API_KEY):
    """Upload a image to imgur using the public API"""
    if getattr(image, 'read'):
        im = image.read()
        image.close()
    else:
        with open(image, 'rb') as (f):
            im = f.read()
    if not api_key:
        raise ApiKeyNotSpecified
    else:
        data = {'key': api_key, 'image': im.encode('base64')}
        request = urllib2.Request(IMGUR_UPLOAD_URL, urllib.urlencode(data))
        response = urllib2.urlopen(request)
        data = json.loads(response.read())
        response.close()
        return data