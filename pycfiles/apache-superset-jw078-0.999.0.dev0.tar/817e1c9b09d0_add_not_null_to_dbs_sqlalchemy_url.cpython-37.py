# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/817e1c9b09d0_add_not_null_to_dbs_sqlalchemy_url.py
# Compiled at: 2020-01-16 19:49:16
# Size of source mod 2**32: 1448 bytes
__doc__ = 'add_not_null_to_dbs_sqlalchemy_url\n\nRevision ID: 817e1c9b09d0\nRevises: db4b49eb0782\nCreate Date: 2019-12-03 10:24:16.201580\n\n'
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