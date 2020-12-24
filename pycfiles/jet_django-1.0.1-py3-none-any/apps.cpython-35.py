# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_django/jet_django/apps.py
# Compiled at: 2019-11-12 07:15:58
# Size of source mod 2**32: 521 bytes
from django.apps import AppConfig

class JetDjangoConfig(AppConfig):
    name = 'jet_django'

    def ready(self):
        from jet_bridge_base import configuration
        from jet_django.configuration import JetDjangoConfiguration
        conf = JetDjangoConfiguration()
        configuration.set_configuration(conf)
        from jet_bridge_base.commands.check_token import check_token_command
        check_token_command('/jet_api/')
        from jet_bridge_base.db import database_connect
        database_connect()