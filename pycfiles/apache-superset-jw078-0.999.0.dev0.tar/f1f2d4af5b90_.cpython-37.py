# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/f1f2d4af5b90_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1418 bytes
__doc__ = 'Enable Filter Select\n\nRevision ID: f1f2d4af5b90\nRevises: e46f2d27a08e\nCreate Date: 2016-11-23 10:27:18.517919\n\n'
revision = 'f1f2d4af5b90'
down_revision = 'e46f2d27a08e'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('datasources', sa.Column('filter_select_enabled', (sa.Boolean()), default=False))
    op.add_column('tables', sa.Column('filter_select_enabled', (sa.Boolean()), default=False))


def downgrade():
    op.drop_column('tables', 'filter_select_enabled')
    op.drop_column('datasources', 'filter_select_enabled')