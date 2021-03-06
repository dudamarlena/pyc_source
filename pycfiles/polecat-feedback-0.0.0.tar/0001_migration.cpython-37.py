# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/polecat_auth/migrations/0001_migration.py
# Compiled at: 2019-07-26 23:12:35
# Size of source mod 2**32: 1062 bytes
from polecat.db.migration import migration, operation
from polecat.db import schema
from polecat.db.schema import column

class Migration(migration.Migration):
    dependencies = []
    operations = [
     operation.CreateRole('admin', parents=[]),
     operation.CreateRole('user', parents=['admin']),
     operation.CreateRole('default', parents=['user']),
     operation.CreateTable('auth_user',
       columns=[
      column.SerialColumn('id', unique=True, null=False, primary_key=True),
      column.TextColumn('name', unique=False, null=True, primary_key=False),
      column.TextColumn('email', unique=True, null=False, primary_key=False, max_length=255),
      column.PasswordColumn('password', unique=False, null=True, primary_key=False),
      column.TimestampColumn('created', unique=False, null=True, primary_key=False, default=(schema.Auto)),
      column.TimestampColumn('logged_out', unique=False, null=True, primary_key=False)])]