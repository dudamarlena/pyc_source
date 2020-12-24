# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/19a814813610_adding_metric_warning_text.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 1502 bytes
"""Adding metric warning_text

Revision ID: 19a814813610
Revises: ca69c70ec99b
Create Date: 2017-09-15 15:09:40.495345

"""
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