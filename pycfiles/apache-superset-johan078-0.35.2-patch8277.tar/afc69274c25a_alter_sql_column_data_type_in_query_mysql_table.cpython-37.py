# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/afc69274c25a_alter_sql_column_data_type_in_query_mysql_table.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2195 bytes
__doc__ = 'update the sql, select_sql, and executed_sql columns in the\n   query table in mysql dbs to be long text columns\n\nRevision ID: afc69274c25a\nRevises: e9df189e5c7e\nCreate Date: 2019-05-06 14:30:26.181449\n\n'
import sqlalchemy as sa
from alembic import op
from sqlalchemy.databases import mysql
from sqlalchemy.dialects.mysql.base import MySQLDialect
revision = 'afc69274c25a'
down_revision = 'e9df189e5c7e'

def upgrade():
    bind = op.get_bind()
    if isinstance(bind.dialect, MySQLDialect):
        with op.batch_alter_table('query') as (batch_op):
            batch_op.alter_column('sql', existing_type=(sa.Text), type_=(mysql.LONGTEXT))
            batch_op.alter_column('select_sql',
              existing_type=(sa.Text), type_=(mysql.LONGTEXT))
            batch_op.alter_column('executed_sql',
              existing_type=(sa.Text), type_=(mysql.LONGTEXT))


def downgrade():
    bind = op.get_bind()
    if isinstance(bind.dialect, MySQLDialect):
        with op.batch_alter_table('query') as (batch_op):
            batch_op.alter_column('sql', existing_type=(mysql.LONGTEXT), type_=(sa.Text))
            batch_op.alter_column('select_sql',
              existing_type=(mysql.LONGTEXT), type_=(sa.Text))
            batch_op.alter_column('executed_sql',
              existing_type=(mysql.LONGTEXT), type_=(sa.Text))