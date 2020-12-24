# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/serverinfo.py
# Compiled at: 2019-10-25 15:25:55
# Size of source mod 2**32: 2170 bytes
from __future__ import absolute_import
import json
from .httpconn import HttpConn
from .config import Config

def getServerInfo(endpoint=None, username=None, password=None, api_key=None, **kwds):
    cfg = Config()
    if endpoint is None:
        if 'hs_endpoint' in cfg:
            endpoint = cfg['hs_endpoint']
    if username is None:
        if 'hs_username' in cfg:
            username = cfg['hs_username']
    if password is None:
        if 'hs_password' in cfg:
            password = cfg['hs_password']
    if api_key is None:
        if 'hs_api_key' in cfg:
            api_key = cfg['hs_api_key']
    http_conn = HttpConn(None, endpoint=endpoint, username=username, password=password, api_key=api_key)
    rsp = http_conn.GET('/about')
    if rsp.status_code == 400:
        rsp = http_conn.GET('/info')
    if rsp.status_code != 200:
        raise IOError(rsp.status_code, rsp.reason)
    rspJson = json.loads(rsp.text)
    rspJson['endpoint'] = endpoint
    rspJson['username'] = username
    if not password:
        rspJson['password'] = ''
    else:
        rspJson['password'] = '*' * len(password)
    http_conn.close()
    http_conn = None
    return rspJson