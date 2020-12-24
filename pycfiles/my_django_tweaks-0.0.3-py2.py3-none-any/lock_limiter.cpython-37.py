# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ricard/develop/my_django_tweaks/my_django_tweaks/test_utils/lock_limiter.py
# Compiled at: 2019-05-17 08:43:05
# Size of source mod 2**32: 2023 bytes
from contextlib import contextmanager
from django.conf import settings
from django.db.models.sql.compiler import SQLCompiler

class WouldSelectMultipleTablesForUpdate(Exception):
    pass


def replacement_as_sql(self, *args, **kwargs):
    sql = (self.query_lock_limiter_old_as_sql)(*args, **kwargs)
    table_names = list(self.query.table_map.keys())
    if self.query.select_for_update:
        if len(table_names) > 1:
            whitelisted = sorted(table_names) in self.query_lock_limiter_whitelist
            if not whitelisted:
                raise WouldSelectMultipleTablesForUpdate(f"Query would select_for_update more than one table: {sql}.  Add {table_names} to settings.TEST_SELECT_FOR_UPDATE_WHITELISTED_TABLE_SETS to allow it.")
    return sql


def patch_sqlcompiler(whitelisted_table_sets):
    SQLCompiler.query_lock_limiter_old_as_sql = SQLCompiler.as_sql
    SQLCompiler.as_sql = replacement_as_sql
    SQLCompiler.query_lock_limiter_whitelist = [sorted(tables) for tables in whitelisted_table_sets]


def unpatch_sqlcompiler():
    SQLCompiler.as_sql = SQLCompiler.query_lock_limiter_old_as_sql
    delattr(SQLCompiler, 'query_lock_limiter_old_as_sql')


@contextmanager
def query_lock_limiter(enable=False, whitelisted_table_sets=[]):
    enabled = enable or getattr(settings, 'TEST_SELECT_FOR_UPDATE_LIMITER_ENABLED', False)
    if not enabled:
        yield
        return
    was_already_patched = hasattr(SQLCompiler, 'query_lock_limiter_old_as_sql')
    if not was_already_patched:
        whitelist = whitelisted_table_sets or getattr(settings, 'TEST_SELECT_FOR_UPDATE_WHITELISTED_TABLE_SETS', [])
        patch_sqlcompiler(whitelist)
    try:
        yield
    finally:
        if not was_already_patched:
            unpatch_sqlcompiler()