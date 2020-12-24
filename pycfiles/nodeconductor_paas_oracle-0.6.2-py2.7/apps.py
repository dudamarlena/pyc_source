# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_paas_oracle/apps.py
# Compiled at: 2016-12-16 07:39:01
from django.apps import AppConfig

class OracleConfig(AppConfig):
    name = 'nodeconductor_paas_oracle'
    verbose_name = 'Oracle'
    service_name = 'Oracle'

    def ready(self):
        from nodeconductor.structure import SupportedServices
        from .backend import OracleBackend
        SupportedServices.register_backend(OracleBackend)