# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dainius/Desktop/scrapyd-dash/scrapyd_dash/operations/tasks_add.py
# Compiled at: 2019-07-07 03:40:51
# Size of source mod 2**32: 455 bytes
import requests

def add_task(project, spider, server, version=None, **kwargs):
    url = 'http://{}:{}/schedule.json'.format(server.ip, server.port)
    data = {'project':project.name, 
     'spider':spider}
    if version:
        data['_version'] = version.version
    data_merged = {**data, **kwargs}
    with requests.Session() as (session):
        try:
            r = session.post(url, data=data_merged)
        except:
            return
            return r.json()