# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\afc69274c25a_alter_sql_column_data_type_in_query_mysql_table.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 2195 bytes
"""update the sql, select_sql, and executed_sql columns in the
   query table in mysql dbs to be long text columns

Revision ID: afc69274c25a
Revises: e9df189e5c7e
Create Date: 2019-05-06 14:30:26.181449

"""
from alembic import op
from sqlalchemy.databases import mysql
from sqlalchemy.dialects.mysql.base import MySQLDialect
import sqlalchemy as sa
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