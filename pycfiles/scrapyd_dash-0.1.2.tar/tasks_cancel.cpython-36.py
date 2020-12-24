# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dainius/Desktop/scrapyd-dash/scrapyd_dash/operations/tasks_cancel.py
# Compiled at: 2019-07-04 07:19:46
# Size of source mod 2**32: 452 bytes
import requests

def cancel_task(server, project, task_id):
    url = 'http://{}:{}/cancel.json'.format(server.ip, server.port)
    data = {'project':project.name, 
     'job':task_id}
    with requests.Session() as (session):
        try:
            r = session.post(url, data=data)
        except:
            return
            return r.json()