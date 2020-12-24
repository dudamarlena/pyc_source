# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/f1f2d4af5b90_.py
# Compiled at: 2019-04-24 13:46:49
# Size of source mod 2**32: 1470 bytes
"""Enable Filter Select

Revision ID: f1f2d4af5b90
Revises: e46f2d27a08e
Create Date: 2016-11-23 10:27:18.517919

"""
revision = 'f1f2d4af5b90'
down_revision = 'e46f2d27a08e'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('datasources', sa.Column('filter_select_enabled', (sa.Boolean()),
      default=False))
    op.add_column('tables', sa.Column('filter_select_enabled', (sa.Boolean()),
      default=False))


def downgrade():
    op.drop_column('tables', 'filter_select_enabled')
    op.drop_column('datasources', 'filter_select_enabled')