# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/4500485bde7d_allow_run_sync_async.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1394 bytes
__doc__ = 'allow_run_sync_async\n\nRevision ID: 4500485bde7d\nRevises: 41f6a59a61f2\nCreate Date: 2016-09-12 23:33:14.789632\n\n'
revision = '4500485bde7d'
down_revision = '41f6a59a61f2'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('dbs', sa.Column('allow_run_async', (sa.Boolean()), nullable=True))
    op.add_column('dbs', sa.Column('allow_run_sync', (sa.Boolean()), nullable=True))


def downgrade():
    try:
        op.drop_column('dbs', 'allow_run_sync')
        op.drop_column('dbs', 'allow_run_async')
    except Exception:
        pass