# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/937d04c16b64_update_datasources.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 1560 bytes
"""update datasources

Revision ID: 937d04c16b64
Revises: d94d33dbe938
Create Date: 2018-07-20 16:08:10.195843

"""
revision = '937d04c16b64'
down_revision = 'd94d33dbe938'
import sqlalchemy as sa
from alembic import op

def upgrade():
    with op.batch_alter_table('datasources') as (batch_op):
        batch_op.alter_column('datasource_name',
          existing_type=(sa.String(255)), nullable=False)


def downgrade():
    with op.batch_alter_table('datasources') as (batch_op):
        batch_op.alter_column('datasource_name',
          existing_type=(sa.String(255)), nullable=True)