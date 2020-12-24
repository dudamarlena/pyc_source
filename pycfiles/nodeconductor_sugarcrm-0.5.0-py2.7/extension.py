# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/extension.py
# Compiled at: 2016-09-28 11:51:43
from nodeconductor.core import NodeConductorExtension

class SugarCRMExtension(NodeConductorExtension):

    @staticmethod
    def django_app():
        return 'nodeconductor_sugarcrm'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in

    @staticmethod
    def celery_tasks():
        from datetime import timedelta
        return {'sugarcrm-sync-crms-quotas': {'task': 'nodeconductor.sugarcrm.sync_crms_quotas', 
                                         'schedule': timedelta(days=1), 
                                         'args': ()}, 
           'sugarcrm-pull-sla': {'task': 'nodeconductor.sugarcrm.pull_sla', 
                                 'schedule': timedelta(minutes=5)}}