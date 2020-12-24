# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/430039611635_log_more.py
# Compiled at: 2019-04-24 13:46:49
# Size of source mod 2**32: 1315 bytes
"""log more

Revision ID: 430039611635
Revises: d827694c7555
Create Date: 2016-02-10 08:47:28.950891

"""
from alembic import op
import sqlalchemy as sa
revision = '430039611635'
down_revision = 'd827694c7555'

def upgrade():
    op.add_column('logs', sa.Column('dashboard_id', (sa.Integer()), nullable=True))
    op.add_column('logs', sa.Column('slice_id', (sa.Integer()), nullable=True))


def downgrade():
    op.drop_column('logs', 'slice_id')
    op.drop_column('logs', 'dashboard_id')