# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/525c854f0005_log_this_plus.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1329 bytes
"""log_this_plus

Revision ID: 525c854f0005
Revises: e46f2d27a08e
Create Date: 2016-12-13 16:19:02.239322

"""
revision = '525c854f0005'
down_revision = 'e46f2d27a08e'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('logs', sa.Column('duration_ms', (sa.Integer()), nullable=True))
    op.add_column('logs', sa.Column('referrer', sa.String(length=1024), nullable=True))


def downgrade():
    op.drop_column('logs', 'referrer')
    op.drop_column('logs', 'duration_ms')