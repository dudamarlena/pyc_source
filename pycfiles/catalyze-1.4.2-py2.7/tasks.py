# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/helpers/tasks.py
# Compiled at: 2015-08-04 23:02:03
from __future__ import absolute_import
import sys, time
from catalyze import config, output

def poll_status(session, env_id, task_id, exit_on_error=True):
    route = '%s/v1/environments/%s/tasks/%s' % (config.paas_host, env_id, task_id)
    while True:
        time.sleep(2)
        task = session.get(route, verify=True)
        if task['status'] not in ('scheduled', 'queued', 'started', 'running'):
            if task['status'] == 'finished':
                return task
            output.write('')
            output.error("Error - ended in status '%s'." % (task['status'],), exit=exit_on_error)
        else:
            output.write('.', sameline=True)