# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/e68c4473c581_allow_multi_schema_metadata_fetch.py
# Compiled at: 2019-04-24 13:46:49
# Size of source mod 2**32: 1360 bytes
"""allow_multi_schema_metadata_fetch

Revision ID: e68c4473c581
Revises: e866bd2d4976
Create Date: 2018-03-06 12:24:30.896293

"""
from alembic import op
import sqlalchemy as sa
revision = 'e68c4473c581'
down_revision = 'e866bd2d4976'

def upgrade():
    op.add_column('dbs', sa.Column('allow_multi_schema_metadata_fetch',
      (sa.Boolean()),
      nullable=True,
      default=True))


def downgrade():
    op.drop_column('dbs', 'allow_multi_schema_metadata_fetch')