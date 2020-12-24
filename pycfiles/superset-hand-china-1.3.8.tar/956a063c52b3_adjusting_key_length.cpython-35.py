# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ljf/superset/superset18/superset/migrations/versions/956a063c52b3_adjusting_key_length.py
# Compiled at: 2017-10-30 08:27:50
# Size of source mod 2**32: 4649 bytes
"""adjusting key length

Revision ID: 956a063c52b3
Revises: f0fbf6129e13
Create Date: 2016-05-11 17:28:32.407340

"""
revision = '956a063c52b3'
down_revision = 'f0fbf6129e13'
from alembic import op
import sqlalchemy as sa

def upgrade():
    with op.batch_alter_table('clusters', schema=None) as (batch_op):
        batch_op.alter_column('broker_endpoint', existing_type=sa.VARCHAR(length=256), type_=sa.String(length=255), existing_nullable=True)
        batch_op.alter_column('broker_host', existing_type=sa.VARCHAR(length=256), type_=sa.String(length=255), existing_nullable=True)
        batch_op.alter_column('coordinator_endpoint', existing_type=sa.VARCHAR(length=256), type_=sa.String(length=255), existing_nullable=True)
        batch_op.alter_column('coordinator_host', existing_type=sa.VARCHAR(length=256), type_=sa.String(length=255), existing_nullable=True)
    with op.batch_alter_table('columns', schema=None) as (batch_op):
        batch_op.alter_column('column_name', existing_type=sa.VARCHAR(length=256), type_=sa.String(length=255), existing_nullable=True)
    with op.batch_alter_table('datasources', schema=None) as (batch_op):
        batch_op.alter_column('datasource_name', existing_type=sa.VARCHAR(length=256), type_=sa.String(length=255), existing_nullable=True)
    with op.batch_alter_table('table_columns', schema=None) as (batch_op):
        batch_op.alter_column('column_name', existing_type=sa.VARCHAR(length=256), type_=sa.String(length=255), existing_nullable=True)
    with op.batch_alter_table('tables', schema=None) as (batch_op):
        batch_op.alter_column('schema', existing_type=sa.VARCHAR(length=256), type_=sa.String(length=255), existing_nullable=True)


def downgrade():
    with op.batch_alter_table('tables', schema=None) as (batch_op):
        batch_op.alter_column('schema', existing_type=sa.String(length=255), type_=sa.VARCHAR(length=256), existing_nullable=True)
    with op.batch_alter_table('table_columns', schema=None) as (batch_op):
        batch_op.alter_column('column_name', existing_type=sa.String(length=255), type_=sa.VARCHAR(length=256), existing_nullable=True)
    with op.batch_alter_table('datasources', schema=None) as (batch_op):
        batch_op.alter_column('datasource_name', existing_type=sa.String(length=255), type_=sa.VARCHAR(length=256), existing_nullable=True)
    with op.batch_alter_table('columns', schema=None) as (batch_op):
        batch_op.alter_column('column_name', existing_type=sa.String(length=255), type_=sa.VARCHAR(length=256), existing_nullable=True)
    with op.batch_alter_table('clusters', schema=None) as (batch_op):
        batch_op.alter_column('coordinator_host', existing_type=sa.String(length=255), type_=sa.VARCHAR(length=256), existing_nullable=True)
        batch_op.alter_column('coordinator_endpoint', existing_type=sa.String(length=255), type_=sa.VARCHAR(length=256), existing_nullable=True)
        batch_op.alter_column('broker_host', existing_type=sa.String(length=255), type_=sa.VARCHAR(length=256), existing_nullable=True)
        batch_op.alter_column('broker_endpoint', existing_type=sa.String(length=255), type_=sa.VARCHAR(length=256), existing_nullable=True)