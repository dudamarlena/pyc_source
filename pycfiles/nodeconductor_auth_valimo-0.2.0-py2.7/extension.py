# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_auth_valimo/extension.py
# Compiled at: 2016-09-19 07:37:17
from __future__ import unicode_literals
from nodeconductor.core import NodeConductorExtension

class AuthValimoExtension(NodeConductorExtension):

    class Settings:
        NODECONCUTOR_AUTH_VALIMO = {b'URL': None, 
           b'AP_ID': None, 
           b'AP_PWD': None, 
           b'DNSName': b'', 
           b'SignatureProfile': None, 
           b'cert_path': None, 
           b'key_path': None, 
           b'message_prefix': b'Login code:'}

    @staticmethod
    def django_app():
        return b'nodeconductor_auth_valimo'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in

    @staticmethod
    def celery_tasks():
        from datetime import timedelta
        return {b'valimo-auth-cleanup-auth-results': {b'task': b'nodeconductor.valimo_auth.cleanup_auth_results', 
                                                 b'schedule': timedelta(hours=1)}}