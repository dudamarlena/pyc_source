# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/817e1c9b09d0_add_not_null_to_dbs_sqlalchemy_url.py
# Compiled at: 2020-01-16 19:49:16
# Size of source mod 2**32: 1448 bytes
"""add_not_null_to_dbs_sqlalchemy_url

Revision ID: 817e1c9b09d0
Revises: db4b49eb0782
Create Date: 2019-12-03 10:24:16.201580

"""
import sqlalchemy as sa
from alembic import op
revision = '817e1c9b09d0'
down_revision = '89115a40e8ea'

def upgrade():
    with op.batch_alter_table('dbs') as (batch_op):
        batch_op.alter_column('sqlalchemy_uri',
          existing_type=sa.VARCHAR(length=1024), nullable=False)


def downgrade():
    with op.batch_alter_table('dbs') as (batch_op):
        batch_op.alter_column('sqlalchemy_uri',
          existing_type=sa.VARCHAR(length=1024), nullable=True)