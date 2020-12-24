# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/quota_classes.py
# Compiled at: 2016-06-13 14:11:03
from vsmclient import base

class QuotaClassSet(base.Resource):

    @property
    def id(self):
        """QuotaClassSet does not have a 'id' attribute but base.Resource
        needs it to self-refresh and QuotaSet is indexed by class_name"""
        return self.class_name

    def update(self, *args, **kwargs):
        self.manager.update(self.class_name, *args, **kwargs)


class QuotaClassSetManager(base.ManagerWithFind):
    resource_class = QuotaClassSet

    def get(self, class_name):
        return self._get('/os-quota-class-sets/%s' % class_name, 'quota_class_set')

    def update(self, class_name, vsms=None, gigabytes=None):
        body = {'quota_class_set': {'class_name': class_name, 
                               'vsms': vsms, 
                               'gigabytes': gigabytes}}
        for key in body['quota_class_set'].keys():
            if body['quota_class_set'][key] is None:
                body['quota_class_set'].pop(key)

        self._update('/os-quota-class-sets/%s' % class_name, body)
        return