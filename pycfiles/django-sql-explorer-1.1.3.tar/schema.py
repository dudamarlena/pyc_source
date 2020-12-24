# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/schema.py
# Compiled at: 2019-07-02 16:47:10
from django.core.cache import cache
from explorer.utils import get_valid_connection
from explorer.tasks import build_schema_cache_async
from explorer.app_settings import EXPLORER_SCHEMA_INCLUDE_TABLE_PREFIXES, EXPLORER_SCHEMA_EXCLUDE_TABLE_PREFIXES, EXPLORER_SCHEMA_INCLUDE_VIEWS, ENABLE_TASKS, EXPLORER_ASYNC_SCHEMA, EXPLORER_CONNECTIONS

def _get_includes():
    return EXPLORER_SCHEMA_INCLUDE_TABLE_PREFIXES


def _get_excludes():
    return EXPLORER_SCHEMA_EXCLUDE_TABLE_PREFIXES


def _include_views():
    return EXPLORER_SCHEMA_INCLUDE_VIEWS is True


def do_async():
    return ENABLE_TASKS and EXPLORER_ASYNC_SCHEMA


def _include_table(t):
    if _get_includes() is not None:
        return any([ t.startswith(p) for p in _get_includes() ])
    return not any([ t.startswith(p) for p in _get_excludes() ])


def connection_schema_cache_key(connection_alias):
    return '_explorer_cache_key_%s' % connection_alias


def schema_info(connection_alias):
    key = connection_schema_cache_key(connection_alias)
    ret = cache.get(key)
    if ret:
        return ret
    if do_async():
        build_schema_cache_async.delay(connection_alias)
    else:
        return build_schema_cache_async(connection_alias)


def build_schema_info(connection_alias):
    """
        Construct schema information via engine-specific queries of the tables in the DB.

        :return: Schema information of the following form, sorted by db_table_name.
            [
                ("db_table_name",
                    [
                        ("db_column_name", "DbFieldType"),
                        (...),
                    ]
                )
            ]

        """
    connection = get_valid_connection(connection_alias)
    ret = []
    with connection.cursor() as (cursor):
        tables_to_introspect = connection.introspection.table_names(cursor, include_views=_include_views())
        for table_name in tables_to_introspect:
            if not _include_table(table_name):
                continue
            td = []
            table_description = connection.introspection.get_table_description(cursor, table_name)
            for row in table_description:
                column_name = row[0]
                try:
                    field_type = connection.introspection.get_field_type(row[1], row)
                except KeyError as e:
                    field_type = 'Unknown'

                td.append((column_name, field_type))

            ret.append((table_name, td))

    return ret


def build_async_schemas():
    if do_async():
        for c in EXPLORER_CONNECTIONS:
            schema_info(c)