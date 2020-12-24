# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/quotas.py
# Compiled at: 2016-06-13 14:11:03
from vsmclient import base

class QuotaSet(base.Resource):

    @property
    def id(self):
        """QuotaSet does not have a 'id' attribute but base.Resource needs it
        to self-refresh and QuotaSet is indexed by tenant_id"""
        return self.tenant_id

    def update(self, *args, **kwargs):
        self.manager.update(self.tenant_id, *args, **kwargs)


class QuotaSetManager(base.ManagerWithFind):
    resource_class = QuotaSet

    def get(self, tenant_id):
        if hasattr(tenant_id, 'tenant_id'):
            tenant_id = tenant_id.tenant_id
        return self._get('/os-quota-sets/%s' % tenant_id, 'quota_set')

    def update(self, tenant_id, vsms=None, snapshots=None, gigabytes=None):
        body = {'quota_set': {'tenant_id': tenant_id, 
                         'vsms': vsms, 
                         'snapshots': snapshots, 
                         'gigabytes': gigabytes}}
        for key in body['quota_set'].keys():
            if body['quota_set'][key] is None:
                body['quota_set'].pop(key)

        self._update('/os-quota-sets/%s' % tenant_id, body)
        return

    def defaults(self, tenant_id):
        return self._get('/os-quota-sets/%s/defaults' % tenant_id, 'quota_set')