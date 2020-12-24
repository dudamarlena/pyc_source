# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/f162a1dea4c4_d3format_by_metric.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1384 bytes
__doc__ = 'd3format_by_metric\n\nRevision ID: f162a1dea4c4\nRevises: 960c69cb1f5b\nCreate Date: 2016-07-06 22:04:28.685100\n\n'
revision = 'f162a1dea4c4'
down_revision = '960c69cb1f5b'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('metrics', sa.Column('d3format', sa.String(length=128), nullable=True))
    op.add_column('sql_metrics', sa.Column('d3format', sa.String(length=128), nullable=True))


def downgrade():
    op.drop_column('sql_metrics', 'd3format')
    op.drop_column('metrics', 'd3format')