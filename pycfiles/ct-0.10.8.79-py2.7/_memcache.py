# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/_memcache.py
# Compiled at: 2017-12-30 20:27:05
import datetime
from cantools.web import respond, succeed, cgi_get, getmem, setmem, delmem, read_file, send_file
from cantools.util import token, transcode
from cantools.hooks import memhook

def response():
    action = cgi_get('action', choices=['get', 'set', 'forget'])
    key = cgi_get('key')
    json = cgi_get('json', default=False)
    mode = cgi_get('mode', default='normal')
    value = cgi_get('value', required=False)
    countdown_list = getmem('_countdown_list', False)
    meta = cgi_get('meta', default={})
    if action == 'forget':
        delmem(key)
    elif action == 'get':
        data = getmem(key, json)
        if mode == 'countdown':
            if key == '_countdown_list':
                succeed(list(countdown_list or set()))
            elif data:
                succeed({'ttl': (data['ttl'] - datetime.datetime.now()).total_seconds(), 
                   'token': data['token'], 
                   'meta': data['meta']})
        elif mode == 'blob':
            send_file(data, detect=True)
        succeed(data)
    elif action == 'set':
        if mode == 'countdown':
            cdl = countdown_list or set()
            cdl.add(key)
            setmem('_countdown_list', cdl, False)
            setmem(key, {'ttl': datetime.datetime.now() + datetime.timedelta(0, value), 
               'token': token(), 
               'meta': meta}, json)
        elif mode == 'blob':
            value = read_file(value)
            if cgi_get('transcode', default=False):
                value = transcode(value, True)
            setmem(key, value, False)
            json = False
        else:
            setmem(key, value, json)
    cgi_get('nohook', default=False) or memhook({'action': action, 
       'key': key, 
       'mode': mode, 
       'json': json, 
       'meta': meta, 
       'value': value, 
       'countdown_list': countdown_list})


respond(response)