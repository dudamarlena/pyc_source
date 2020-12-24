# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/7467e77870e4_remove_aggs.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 2400 bytes
"""remove_aggs

Revision ID: 7467e77870e4
Revises: c829ff0b37d0
Create Date: 2018-07-22 08:50:01.078218

"""
import sqlalchemy as sa
from alembic import op
revision = '7467e77870e4'
down_revision = 'c829ff0b37d0'

def upgrade():
    with op.batch_alter_table('table_columns') as (batch_op):
        batch_op.drop_column('avg')
        batch_op.drop_column('max')
        batch_op.drop_column('sum')
        batch_op.drop_column('count_distinct')
        batch_op.drop_column('min')
    with op.batch_alter_table('columns') as (batch_op):
        batch_op.drop_column('avg')
        batch_op.drop_column('max')
        batch_op.drop_column('sum')
        batch_op.drop_column('count_distinct')
        batch_op.drop_column('min')


def downgrade():
    op.add_column('table_columns', sa.Column('min', (sa.Boolean()), nullable=True))
    op.add_column('table_columns', sa.Column('count_distinct', (sa.Boolean()), nullable=True))
    op.add_column('table_columns', sa.Column('sum', (sa.Boolean()), nullable=True))
    op.add_column('table_columns', sa.Column('max', (sa.Boolean()), nullable=True))
    op.add_column('table_columns', sa.Column('avg', (sa.Boolean()), nullable=True))
    op.add_column('columns', sa.Column('min', (sa.Boolean()), nullable=True))
    op.add_column('columns', sa.Column('count_distinct', (sa.Boolean()), nullable=True))
    op.add_column('columns', sa.Column('sum', (sa.Boolean()), nullable=True))
    op.add_column('columns', sa.Column('max', (sa.Boolean()), nullable=True))
    op.add_column('columns', sa.Column('avg', (sa.Boolean()), nullable=True))