# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/30bb17c0dc76_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1319 bytes
__doc__ = 'empty message\n\nRevision ID: 30bb17c0dc76\nRevises: f231d82b9b26\nCreate Date: 2018-04-08 07:34:12.149910\n\n'
revision = '30bb17c0dc76'
down_revision = 'f231d82b9b26'
from datetime import date
import sqlalchemy as sa
from alembic import op

def upgrade():
    with op.batch_alter_table('logs') as (batch_op):
        batch_op.drop_column('dt')


def downgrade():
    with op.batch_alter_table('logs') as (batch_op):
        batch_op.add_column(sa.Column('dt', (sa.Date), default=(date.today())))