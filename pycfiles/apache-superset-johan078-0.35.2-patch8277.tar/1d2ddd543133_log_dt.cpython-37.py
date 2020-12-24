# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/1d2ddd543133_log_dt.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1173 bytes
__doc__ = 'log dt\n\nRevision ID: 1d2ddd543133\nRevises: d2424a248d63\nCreate Date: 2016-03-25 14:35:44.642576\n\n'
revision = '1d2ddd543133'
down_revision = 'd2424a248d63'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('logs', sa.Column('dt', (sa.Date()), nullable=True))


def downgrade():
    op.drop_column('logs', 'dt')