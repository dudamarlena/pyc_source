# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/apps.py
# Compiled at: 2015-12-07 14:10:29
# Size of source mod 2**32: 3227 bytes
import sys, django
from django.conf import settings
from django.db.backends.signals import connection_created
from django.apps import AppConfig
from psycopg2.extras import register_hstore
HSTORE_REGISTER_GLOBALLY = getattr(settings, 'DJANGO_HSTORE_ADAPTER_REGISTRATION', 'global') == 'global'
CONNECTION_CREATED_SIGNAL_WEAKREF = bool(getattr(settings, 'DJANGO_HSTORE_ADAPTER_SIGNAL_WEAKREF', False))
GEODJANGO_INSTALLED = False
for database in settings.DATABASES.values():
    if 'postgis' in database.get('ENGINE'):
        GEODJANGO_INSTALLED = True
        break

class ConnectionCreateHandler(object):
    __doc__ = '\n    Generic connection handlers manager.\n    Executes attached functions when connection is created.\n    With possibility of attaching single execution methods.\n    '
    generic_handlers = []
    unique_handlers = []

    def __call__(self, sender, connection, **kwargs):
        handlers = set()
        if len(self.unique_handlers) > 0:
            handlers.update(self.unique_handlers)
            self.unique_handlers = []
        handlers.update(self.generic_handlers)
        return [x(connection) for x in handlers]

    def attach_handler(self, func, vendor=None, unique=False):
        if unique:
            self.unique_handlers.append(func)
        else:
            self.generic_handlers.append(func)


connection_handler = ConnectionCreateHandler()

def register_hstore_handler(connection, **kwargs):
    if connection.vendor != 'postgresql' or connection.settings_dict.get('HAS_HSTORE', True) is False:
        return
    if connection.settings_dict['NAME'] is None:
        connection_handler.attach_handler(register_hstore_handler, vendor='postgresql', unique=HSTORE_REGISTER_GLOBALLY)
        return
    if sys.version_info[0] < 3:
        register_hstore(connection.connection, globally=HSTORE_REGISTER_GLOBALLY, unicode=True)
    else:
        register_hstore(connection.connection, globally=HSTORE_REGISTER_GLOBALLY)


connection_handler.attach_handler(register_hstore_handler, vendor='postgresql', unique=HSTORE_REGISTER_GLOBALLY)

class HStoreConfig(AppConfig):
    name = 'django_hstore'
    verbose = 'Django HStore'

    def ready(self):
        connection_created.connect(connection_handler, weak=CONNECTION_CREATED_SIGNAL_WEAKREF, dispatch_uid='_connection_create_handler')