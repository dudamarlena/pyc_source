# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/0b1f1ab473c0_add_extra_column_to_query.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1316 bytes
__doc__ = 'Add extra column to Query\n\nRevision ID: 0b1f1ab473c0\nRevises: 55e910a74826\nCreate Date: 2018-11-05 08:42:56.181012\n\n'
import sqlalchemy as sa
from alembic import op
revision = '0b1f1ab473c0'
down_revision = '55e910a74826'

def upgrade():
    with op.batch_alter_table('query') as (batch_op):
        batch_op.add_column(sa.Column('extra_json', (sa.Text()), nullable=True))


def downgrade():
    with op.batch_alter_table('query') as (batch_op):
        batch_op.drop_column('extra_json')