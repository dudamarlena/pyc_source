# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/19a814813610_adding_metric_warning_text.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1502 bytes
__doc__ = 'Adding metric warning_text\n\nRevision ID: 19a814813610\nRevises: ca69c70ec99b\nCreate Date: 2017-09-15 15:09:40.495345\n\n'
revision = '19a814813610'
down_revision = 'ca69c70ec99b'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('metrics', sa.Column('warning_text', (sa.Text()), nullable=True))
    op.add_column('sql_metrics', sa.Column('warning_text', (sa.Text()), nullable=True))


def downgrade():
    with op.batch_alter_table('sql_metrics') as (batch_op_sql_metrics):
        batch_op_sql_metrics.drop_column('warning_text')
    with op.batch_alter_table('metrics') as (batch_op_metrics):
        batch_op_metrics.drop_column('warning_text')