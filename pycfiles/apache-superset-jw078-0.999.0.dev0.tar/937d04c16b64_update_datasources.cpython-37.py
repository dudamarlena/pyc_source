# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/937d04c16b64_update_datasources.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1560 bytes
__doc__ = 'update datasources\n\nRevision ID: 937d04c16b64\nRevises: d94d33dbe938\nCreate Date: 2018-07-20 16:08:10.195843\n\n'
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