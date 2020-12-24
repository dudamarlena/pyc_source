# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/11c737c17cc6_deprecate_restricted_metrics.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1487 bytes
__doc__ = 'deprecate_restricted_metrics\n\nRevision ID: 11c737c17cc6\nRevises: def97f26fdfb\nCreate Date: 2019-09-08 21:50:58.200229\n\n'
import sqlalchemy as sa
from alembic import op
revision = '11c737c17cc6'
down_revision = 'def97f26fdfb'

def upgrade():
    with op.batch_alter_table('metrics') as (batch_op):
        batch_op.drop_column('is_restricted')
    with op.batch_alter_table('sql_metrics') as (batch_op):
        batch_op.drop_column('is_restricted')


def downgrade():
    op.add_column('sql_metrics', sa.Column('is_restricted', (sa.BOOLEAN()), nullable=True))
    op.add_column('metrics', sa.Column('is_restricted', (sa.BOOLEAN()), nullable=True))