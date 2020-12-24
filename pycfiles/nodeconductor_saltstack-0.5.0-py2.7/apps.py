# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/apps.py
# Compiled at: 2016-09-28 02:05:53
from django.apps import AppConfig
from nodeconductor.structure import SupportedServices

class SaltStackConfig(AppConfig):
    name = 'nodeconductor_saltstack.sharepoint'
    verbose_name = 'SaltStack SharePoint'
    service_name = 'SaltStack'

    def ready(self):
        from .backend import SharepointBackend
        SupportedServices.register_backend(SharepointBackend, nested=True)