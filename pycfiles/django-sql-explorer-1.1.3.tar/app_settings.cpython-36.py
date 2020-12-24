# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/app_settings.py
# Compiled at: 2019-07-02 16:47:10
# Size of source mod 2**32: 4129 bytes
from django.conf import settings
EXPLORER_CONNECTIONS = getattr(settings, 'EXPLORER_CONNECTIONS', {})
EXPLORER_DEFAULT_CONNECTION = getattr(settings, 'EXPLORER_DEFAULT_CONNECTION', None)
EXPLORER_SQL_BLACKLIST = getattr(settings, 'EXPLORER_SQL_BLACKLIST', ('ALTER', 'RENAME ',
                                                                      'DROP', 'TRUNCATE',
                                                                      'INSERT INTO',
                                                                      'UPDATE', 'REPLACE',
                                                                      'DELETE', 'CREATE TABLE',
                                                                      'GRANT', 'OWNER TO'))
EXPLORER_SQL_WHITELIST = getattr(settings, 'EXPLORER_SQL_WHITELIST', ('CREATED', 'UPDATED',
                                                                      'DELETED',
                                                                      'REGEXP_REPLACE'))
EXPLORER_DEFAULT_ROWS = getattr(settings, 'EXPLORER_DEFAULT_ROWS', 1000)
EXPLORER_SCHEMA_EXCLUDE_TABLE_PREFIXES = getattr(settings, 'EXPLORER_SCHEMA_EXCLUDE_TABLE_PREFIXES', ('auth_',
                                                                                                      'contenttypes_',
                                                                                                      'sessions_',
                                                                                                      'admin_'))
EXPLORER_SCHEMA_INCLUDE_TABLE_PREFIXES = getattr(settings, 'EXPLORER_SCHEMA_INCLUDE_TABLE_PREFIXES', None)
EXPLORER_SCHEMA_INCLUDE_VIEWS = getattr(settings, 'EXPLORER_SCHEMA_INCLUDE_VIEWS', False)
EXPLORER_TRANSFORMS = getattr(settings, 'EXPLORER_TRANSFORMS', [])
EXPLORER_PERMISSION_VIEW = getattr(settings, 'EXPLORER_PERMISSION_VIEW', lambda u: u.is_staff)
EXPLORER_PERMISSION_CHANGE = getattr(settings, 'EXPLORER_PERMISSION_CHANGE', lambda u: u.is_staff)
EXPLORER_RECENT_QUERY_COUNT = getattr(settings, 'EXPLORER_RECENT_QUERY_COUNT', 10)
EXPLORER_ASYNC_SCHEMA = getattr(settings, 'EXPLORER_ASYNC_SCHEMA', False)
EXPLORER_DATA_EXPORTERS = getattr(settings, 'EXPLORER_DATA_EXPORTERS', [
 ('csv', 'explorer.exporters.CSVExporter'),
 ('excel', 'explorer.exporters.ExcelExporter'),
 ('json', 'explorer.exporters.JSONExporter')])
CSV_DELIMETER = getattr(settings, 'EXPLORER_CSV_DELIMETER', ',')
EXPLORER_TOKEN = getattr(settings, 'EXPLORER_TOKEN', 'CHANGEME')
EXPLORER_GET_USER_QUERY_VIEWS = lambda : getattr(settings, 'EXPLORER_USER_QUERY_VIEWS', {})
EXPLORER_TOKEN_AUTH_ENABLED = lambda : getattr(settings, 'EXPLORER_TOKEN_AUTH_ENABLED', False)
ENABLE_TASKS = getattr(settings, 'EXPLORER_TASKS_ENABLED', False)
S3_ACCESS_KEY = getattr(settings, 'EXPLORER_S3_ACCESS_KEY', None)
S3_SECRET_KEY = getattr(settings, 'EXPLORER_S3_SECRET_KEY', None)
S3_BUCKET = getattr(settings, 'EXPLORER_S3_BUCKET', None)
FROM_EMAIL = getattr(settings, 'EXPLORER_FROM_EMAIL', 'django-sql-explorer@example.com')
UNSAFE_RENDERING = getattr(settings, 'EXPLORER_UNSAFE_RENDERING', False)