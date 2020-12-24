# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/ad4d656d92bc_add_avg_metric.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1438 bytes
__doc__ = 'Add avg() to default metrics\n\nRevision ID: ad4d656d92bc\nRevises: b46fa1b0b39e\nCreate Date: 2016-10-25 10:16:39.871078\n\n'
revision = 'ad4d656d92bc'
down_revision = '7e3ddad2a00b'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('columns', sa.Column('avg', (sa.Boolean()), nullable=True))
    op.add_column('table_columns', sa.Column('avg', (sa.Boolean()), nullable=True))


def downgrade():
    with op.batch_alter_table('columns') as (batch_op):
        batch_op.drop_column('avg')
    with op.batch_alter_table('table_columns') as (batch_op):
        batch_op.drop_column('avg')