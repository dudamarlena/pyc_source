# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/7467e77870e4_remove_aggs.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2400 bytes
__doc__ = 'remove_aggs\n\nRevision ID: 7467e77870e4\nRevises: c829ff0b37d0\nCreate Date: 2018-07-22 08:50:01.078218\n\n'
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