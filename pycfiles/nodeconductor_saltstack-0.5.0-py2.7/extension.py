# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/extension.py
# Compiled at: 2016-09-28 02:05:53
from nodeconductor.core import NodeConductorExtension

class SharepointExtension(NodeConductorExtension):

    @staticmethod
    def django_app():
        return 'nodeconductor_saltstack.sharepoint'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in

    @staticmethod
    def celery_tasks():
        from datetime import timedelta
        return {'sharepoint-sync-tenants': {'task': 'nodeconductor.sharepoint.sync_tenants', 
                                       'schedule': timedelta(minutes=10), 
                                       'args': ()}}