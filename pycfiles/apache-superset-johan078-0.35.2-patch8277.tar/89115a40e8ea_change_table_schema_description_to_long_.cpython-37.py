# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/89115a40e8ea_change_table_schema_description_to_long_.py
# Compiled at: 2020-01-16 19:49:16
# Size of source mod 2**32: 1723 bytes
__doc__ = 'Change table schema description to long text\n\nRevision ID: 89115a40e8ea\nRevises: 5afa9079866a\nCreate Date: 2019-12-03 13:50:24.746867\n\n'
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