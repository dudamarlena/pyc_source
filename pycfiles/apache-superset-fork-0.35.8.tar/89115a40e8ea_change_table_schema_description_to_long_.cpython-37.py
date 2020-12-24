# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/89115a40e8ea_change_table_schema_description_to_long_.py
# Compiled at: 2020-01-16 19:49:16
# Size of source mod 2**32: 1723 bytes
"""Change table schema description to long text

Revision ID: 89115a40e8ea
Revises: 5afa9079866a
Create Date: 2019-12-03 13:50:24.746867

"""
revision = '89115a40e8ea'
down_revision = '5afa9079866a'
import sqlalchemy as sa
from alembic import op
from sqlalchemy.databases import mysql
from sqlalchemy.dialects.mysql.base import MySQLDialect

def upgrade():
    bind = op.get_bind()
    if isinstance(bind.dialect, MySQLDialect):
        with op.batch_alter_table('table_schema') as (batch_op):
            batch_op.alter_column('description',
              existing_type=(sa.Text), type_=(mysql.LONGTEXT))


def downgrade():
    bind = op.get_bind()
    if isinstance(bind.dialect, MySQLDialect):
        with op.batch_alter_table('table_schema') as (batch_op):
            batch_op.alter_column('description',
              existing_type=(mysql.LONGTEXT), type_=(sa.Text))