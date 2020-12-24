# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/4500485bde7d_allow_run_sync_async.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 1394 bytes
"""allow_run_sync_async

Revision ID: 4500485bde7d
Revises: 41f6a59a61f2
Create Date: 2016-09-12 23:33:14.789632

"""
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