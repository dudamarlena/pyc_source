# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pyhomee/util.py
# Compiled at: 2018-11-10 05:14:24
# Size of source mod 2**32: 541 bytes
import requests, hashlib

def get_token(hostname, username, password):
    url = 'http://{}:7681/access_token'.format(hostname)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    form = {'device_name':'Home Assistant', 
     'device_hardware_id':'homeassistant', 
     'device_os':5, 
     'device_type':3, 
     'device_app':1}
    auth = (
     username, hashlib.sha512(password).hexdigest())
    r = requests.post(url, auth=auth, data=form)
    return r.text.split('&')[0].split('=')[1]