# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dainius/Desktop/scrapyd-dash/scrapyd_dash/operations/versions_list.py
# Compiled at: 2019-07-06 04:02:45
# Size of source mod 2**32: 525 bytes
import requests, json

def versions_list(server, project='default'):
    full_url = 'http://{}:{}/listversions.json?project={}'.format(server.ip, server.port, project)
    timeout = 5
    with requests.Session() as (session):
        try:
            r = session.get(full_url, timeout=timeout)
        except:
            return
            data = json.loads(r.text)
            return data.get('versions', [])