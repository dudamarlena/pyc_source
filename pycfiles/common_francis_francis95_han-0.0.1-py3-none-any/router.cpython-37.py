# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """DatabaseOverrideRouter"""

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
    """database_override"""

    def __init__(self, using=None, read=True, write=False, **options):
        self.read = read
        self.write = write
        self.database_alias = None
        if not using:
            if options:
                using = deepcopy(connections.databases.get(DEFAULT_DB_ALIAS))
        elif isinstance(using, str):
            self.using = using
        elif isinstance(using, dict):
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