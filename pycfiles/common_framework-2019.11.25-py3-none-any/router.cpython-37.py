# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/router.py
# Compiled at: 2018-02-03 12:24:20
# Size of source mod 2**32: 4885 bytes
import threading, sys
from copy import deepcopy
from functools import wraps
from common.utils import short_identifier
from django.db import connections, DEFAULT_DB_ALIAS
local_thread = threading.local()

class DatabaseOverrideRouter(object):
    __doc__ = '\n    Database router which route read and write queries through user-defined database connections\n    '

    def db_for_read(self, model, **hints):
        if sys.argv[1:2] == ['test']:
            return DEFAULT_DB_ALIAS
        return getattr(local_thread, 'db_read_override', [DEFAULT_DB_ALIAS])[(-1)]

    def db_for_write(self, model, **hints):
        if sys.argv[1:2] == ['test']:
            return DEFAULT_DB_ALIAS
        return getattr(local_thread, 'db_write_override', [DEFAULT_DB_ALIAS])[(-1)]

    def allow_relation(self, *args, **kwargs):
        return True

    def allow_syncdb(self, *args, **kwargs):
        pass

    def allow_migrate(self, *args, **kwargs):
        pass


class database_override:
    __doc__ = "\n    A decorator and context manager to do queries on a given database.\n\n    :type using: str or dict, optional\n    :param using: The database to run queries on.\n        A string will route through the matching database in ``django.conf.settings.DATABASES``.\n        A dictionary will set up a connection with the given configuration and route queries to it.\n        If None, the ``'default'`` database connection will be used.\n\n    :type read: bool, optional\n    :param read: Controls whether database reads will route through the provided database connection.\n        If ``False``, reads will route through the ``'default'`` database connection. Defaults to ``True``.\n\n    :type write: bool, optional\n    :param write: Controls whether database writes will route to the provided database connection.\n        If ``False``, writes will route through the ``'default'`` database connection. Defaults to ``False``.\n\n    :type options: dict, optional\n    :param options: Custom options to apply on the given or default database connection.\n        Could be defined through the ``using`` parameter as dictionary for new database connection,\n        but can alter existing connection options if ``using`` is either a string or None.\n\n    Usage as a context manager:\n\n    .. code-block:: python\n        from my_django_app.utils import tricky_query\n        with override_database('database_1'):\n            results = tricky_query()\n\n    Usage as a decorator:\n\n    .. code-block:: python\n        from my_django_app.models import Account\n        @override_database('database_2')\n        def lowest_id_account():\n            Account.objects.order_by('-id')[0]\n\n    Used with a configuration dictionary:\n\n    .. code-block:: python\n        db_config = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'path/to/mydatabase.db'}\n        with override_database(db_config):\n            # Run queries\n    "

    def __init__(self, using=None, read=True, write=False, **options):
        self.read = read
        self.write = write
        self.database_alias = None
        if not using:
            if options:
                using = deepcopy(connections.databases.get(DEFAULT_DB_ALIAS))
        elif isinstance(using, str):
            self.using = using
        else:
            if isinstance(using, dict):
                if options:
                    database_options = using['OPTIONS'] = using.get('OPTIONS', {})
                    (database_options.update)(**options)
                self.database_alias = short_identifier()
                connections.databases[self.database_alias] = using
                self.using = self.database_alias

    def __enter__(self):
        if not hasattr(local_thread, 'db_read_override'):
            local_thread.db_read_override = [
             DEFAULT_DB_ALIAS]
        if not hasattr(local_thread, 'db_write_override'):
            local_thread.db_write_override = [
             DEFAULT_DB_ALIAS]
        read_db = self.using if self.read else local_thread.db_read_override[(-1)]
        write_db = self.using if self.write else local_thread.db_write_override[(-1)]
        local_thread.db_read_override.append(read_db)
        local_thread.db_write_override.append(write_db)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        local_thread.db_read_override.pop()
        local_thread.db_write_override.pop()
        if self.database_alias:
            connections[self.database_alias].close()
            del connections.databases[self.database_alias]

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper