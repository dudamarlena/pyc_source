# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/430039611635_log_more.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1315 bytes
__doc__ = 'log more\n\nRevision ID: 430039611635\nRevises: d827694c7555\nCreate Date: 2016-02-10 08:47:28.950891\n\n'
import sqlalchemy as sa
from alembic import op
revision = '430039611635'
down_revision = 'd827694c7555'

def upgrade():
    op.add_column('logs', sa.Column('dashboard_id', (sa.Integer()), nullable=True))
    op.add_column('logs', sa.Column('slice_id', (sa.Integer()), nullable=True))


def downgrade():
    op.drop_column('logs', 'slice_id')
    op.drop_column('logs', 'dashboard_id')