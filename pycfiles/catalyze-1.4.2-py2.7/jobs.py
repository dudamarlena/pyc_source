# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/helpers/jobs.py
# Compiled at: 2015-08-04 23:02:03
from __future__ import absolute_import
from catalyze import config, output

def list(session, env_id, svc_id):
    route = '%s/v1/environments/%s/services/%s/jobs' % (config.paas_host, env_id, svc_id)
    return session.get(route, verify=True)


def retrieve(session, env_id, svc_id, job_id):
    route = '%s/v1/environments/%s/services/%s/jobs/%s' % (config.paas_host, env_id, svc_id, job_id)
    return session.get(route, verify=True)


def poll_until_complete(session, env_id, svc_id, job_id):
    while True:
        job = retrieve(session, env_id, svc_id, job_id)
        if job['status'] not in ('scheduled', 'queued', 'started', 'running'):
            if job['status'] == 'finished':
                return job
            output.error("\nJob ended in status '%s'. Check log for details.")
            sys.exit(1)
            break
        sys.stdout.write('.')
        time.sleep(2)


def retrieve_from_task_id(session, env_id, task_id):
    route = '%s/v1/environments/%s/tasks/%s' % (config.paas_host, env_id, task_id)
    return session.get(route, verify=True)