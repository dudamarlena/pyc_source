# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ljf/superset/superset18/superset/migrations/versions/f162a1dea4c4_d3format_by_metric.py
# Compiled at: 2017-10-30 08:27:50
# Size of source mod 2**32: 571 bytes
"""d3format_by_metric

Revision ID: f162a1dea4c4
Revises: 960c69cb1f5b
Create Date: 2016-07-06 22:04:28.685100

"""
revision = 'f162a1dea4c4'
down_revision = '960c69cb1f5b'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('metrics', sa.Column('d3format', sa.String(length=128), nullable=True))
    op.add_column('sql_metrics', sa.Column('d3format', sa.String(length=128), nullable=True))


def downgrade():
    op.drop_column('sql_metrics', 'd3format')
    op.drop_column('metrics', 'd3format')