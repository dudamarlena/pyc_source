# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/2591d77e9831_user_id.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1426 bytes
__doc__ = 'user_id\n\nRevision ID: 2591d77e9831\nRevises: 12d55656cbca\nCreate Date: 2015-12-15 17:02:45.128709\n\n'
revision = '2591d77e9831'
down_revision = '12d55656cbca'
import sqlalchemy as sa
from alembic import op

def upgrade():
    with op.batch_alter_table('tables') as (batch_op):
        batch_op.add_column(sa.Column('user_id', sa.Integer()))
        batch_op.create_foreign_key('user_id', 'ab_user', ['user_id'], ['id'])


def downgrade():
    with op.batch_alter_table('tables') as (batch_op):
        batch_op.drop_constraint('user_id', type_='foreignkey')
        batch_op.drop_column('user_id')