# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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