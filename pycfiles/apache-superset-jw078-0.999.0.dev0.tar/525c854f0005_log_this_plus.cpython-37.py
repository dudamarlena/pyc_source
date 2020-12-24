# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/525c854f0005_log_this_plus.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1329 bytes
__doc__ = 'log_this_plus\n\nRevision ID: 525c854f0005\nRevises: e46f2d27a08e\nCreate Date: 2016-12-13 16:19:02.239322\n\n'
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