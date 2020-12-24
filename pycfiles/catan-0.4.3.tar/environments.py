# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/helpers/environments.py
# Compiled at: 2015-08-04 23:59:02
from __future__ import absolute_import
from catalyze import config, output

def list(session):
    route = '%s/v1/environments?pageSize=1000' % (config.paas_host,)
    return session.get(route, verify=True)


def retrieve(session, env_id, source='spec'):
    route = '%s/v1/environments/%s?source=%s' % (config.paas_host, env_id, source)
    return session.get(route, verify=True)


def list_users(session, env_id):
    route = '%s/v1/environments/%s/users' % (config.paas_host, env_id)
    return session.get(route, verify=True)


def add_user(session, env_id, user_id):
    route = '%s/v1/environments/%s/users/%s' % (config.paas_host, env_id, user_id)
    return session.post(route, {}, verify=True)


def remove_user(session, env_id, user_id):
    route = '%s/v1/environments/%s/users/%s' % (config.paas_host, env_id, user_id)
    return session.delete(route, verify=True)


def retrieve_metrics(session, env_id, mins=1):
    route = '%s/v1/environments/%s/metrics?mins=%d' % (config.paas_host, env_id, mins)
    return session.get(route, verify=True)