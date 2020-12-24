# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/d7c1a0d6f2da_remove_limit_used_from_query_model.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1276 bytes
__doc__ = 'Remove limit used from query model\n\nRevision ID: d7c1a0d6f2da\nRevises: afc69274c25a\nCreate Date: 2019-06-04 10:12:36.675369\n\n'
revision = 'd7c1a0d6f2da'
down_revision = 'afc69274c25a'
import sqlalchemy as sa
from alembic import op

def upgrade():
    with op.batch_alter_table('query') as (batch_op):
        batch_op.drop_column('limit_used')


def downgrade():
    op.add_column('query', sa.Column('limit_used', (sa.BOOLEAN()), nullable=True))