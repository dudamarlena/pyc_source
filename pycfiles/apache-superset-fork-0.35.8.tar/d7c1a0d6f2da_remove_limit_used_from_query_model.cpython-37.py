# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/d7c1a0d6f2da_remove_limit_used_from_query_model.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1276 bytes
"""Remove limit used from query model

Revision ID: d7c1a0d6f2da
Revises: afc69274c25a
Create Date: 2019-06-04 10:12:36.675369

"""
revision = 'd7c1a0d6f2da'
down_revision = 'afc69274c25a'
import sqlalchemy as sa
from alembic import op

def upgrade():
    with op.batch_alter_table('query') as (batch_op):
        batch_op.drop_column('limit_used')


def downgrade():
    op.add_column('query', sa.Column('limit_used', (sa.BOOLEAN()), nullable=True))