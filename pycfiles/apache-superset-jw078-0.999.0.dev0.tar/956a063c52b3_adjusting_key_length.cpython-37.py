# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/956a063c52b3_adjusting_key_length.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 4937 bytes
__doc__ = 'adjusting key length\n\nRevision ID: 956a063c52b3\nRevises: f0fbf6129e13\nCreate Date: 2016-05-11 17:28:32.407340\n\n'
import sqlalchemy as sa
from alembic import op
revision = '956a063c52b3'
down_revision = 'f0fbf6129e13'

def upgrade():
    with op.batch_alter_table('clusters', schema=None) as (batch_op):
        batch_op.alter_column('broker_endpoint',
          existing_type=sa.VARCHAR(length=256),
          type_=sa.String(length=255),
          existing_nullable=True)
        batch_op.alter_column('broker_host',
          existing_type=sa.VARCHAR(length=256),
          type_=sa.String(length=255),
          existing_nullable=True)
        batch_op.alter_column('coordinator_endpoint',
          existing_type=sa.VARCHAR(length=256),
          type_=sa.String(length=255),
          existing_nullable=True)
        batch_op.alter_column('coordinator_host',
          existing_type=sa.VARCHAR(length=256),
          type_=sa.String(length=255),
          existing_nullable=True)
    with op.batch_alter_table('columns', schema=None) as (batch_op):
        batch_op.alter_column('column_name',
          existing_type=sa.VARCHAR(length=256),
          type_=sa.String(length=255),
          existing_nullable=True)
    with op.batch_alter_table('datasources', schema=None) as (batch_op):
        batch_op.alter_column('datasource_name',
          existing_type=sa.VARCHAR(length=256),
          type_=sa.String(length=255),
          existing_nullable=True)
    with op.batch_alter_table('table_columns', schema=None) as (batch_op):
        batch_op.alter_column('column_name',
          existing_type=sa.VARCHAR(length=256),
          type_=sa.String(length=255),
          existing_nullable=True)
    with op.batch_alter_table('tables', schema=None) as (batch_op):
        batch_op.alter_column('schema',
          existing_type=sa.VARCHAR(length=256),
          type_=sa.String(length=255),
          existing_nullable=True)


def downgrade():
    with op.batch_alter_table('tables', schema=None) as (batch_op):
        batch_op.alter_column('schema',
          existing_type=sa.String(length=255),
          type_=sa.VARCHAR(length=256),
          existing_nullable=True)
    with op.batch_alter_table('table_columns', schema=None) as (batch_op):
        batch_op.alter_column('column_name',
          existing_type=sa.String(length=255),
          type_=sa.VARCHAR(length=256),
          existing_nullable=True)
    with op.batch_alter_table('datasources', schema=None) as (batch_op):
        batch_op.alter_column('datasource_name',
          existing_type=sa.String(length=255),
          type_=sa.VARCHAR(length=256),
          existing_nullable=True)
    with op.batch_alter_table('columns', schema=None) as (batch_op):
        batch_op.alter_column('column_name',
          existing_type=sa.String(length=255),
          type_=sa.VARCHAR(length=256),
          existing_nullable=True)
    with op.batch_alter_table('clusters', schema=None) as (batch_op):
        batch_op.alter_column('coordinator_host',
          existing_type=sa.String(length=255),
          type_=sa.VARCHAR(length=256),
          existing_nullable=True)
        batch_op.alter_column('coordinator_endpoint',
          existing_type=sa.String(length=255),
          type_=sa.VARCHAR(length=256),
          existing_nullable=True)
        batch_op.alter_column('broker_host',
          existing_type=sa.String(length=255),
          type_=sa.VARCHAR(length=256),
          existing_nullable=True)
        batch_op.alter_column('broker_endpoint',
          existing_type=sa.String(length=255),
          type_=sa.VARCHAR(length=256),
          existing_nullable=True)