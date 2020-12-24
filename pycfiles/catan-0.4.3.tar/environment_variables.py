# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/helpers/environment_variables.py
# Compiled at: 2015-06-29 10:16:09
from __future__ import absolute_import
from catalyze import config

def list(session, env_id, svc_id):
    route = '%s/v1/environments/%s/services/%s/env' % (config.paas_host, env_id, svc_id)
    return session.get(route, verify=True)


def set(session, env_id, svc_id, body):
    route = '%s/v1/environments/%s/services/%s/env' % (config.paas_host, env_id, svc_id)
    return session.post(route, body, verify=True)


def unset(session, env_id, svc_id, key):
    route = '%s/v1/environments/%s/services/%s/env/%s' % (config.paas_host, env_id, svc_id, key)
    return session.delete(route, verify=True)