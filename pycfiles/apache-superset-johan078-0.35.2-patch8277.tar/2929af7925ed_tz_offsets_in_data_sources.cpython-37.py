# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/2929af7925ed_tz_offsets_in_data_sources.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1334 bytes
__doc__ = 'TZ offsets in data sources\n\nRevision ID: 2929af7925ed\nRevises: 1e2841a4128\nCreate Date: 2015-10-19 20:54:00.565633\n\n'
revision = '2929af7925ed'
down_revision = '1e2841a4128'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('datasources', sa.Column('offset', (sa.Integer()), nullable=True))
    op.add_column('tables', sa.Column('offset', (sa.Integer()), nullable=True))


def downgrade():
    op.drop_column('tables', 'offset')
    op.drop_column('datasources', 'offset')