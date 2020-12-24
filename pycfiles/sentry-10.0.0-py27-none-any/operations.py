# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/db/postgres/operations.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.db.backends.postgresql_psycopg2.base import DatabaseOperations

class DatabaseOperations(DatabaseOperations):

    def field_cast_sql(self, db_type, internal_type):
        return '%s'