# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/cefabc8f7d38_increase_size_of_name_column_in_ab_view_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1660 bytes
__doc__ = 'Increase size of name column in ab_view_menu\n\nRevision ID: cefabc8f7d38\nRevises: 6c7537a6004a\nCreate Date: 2018-12-13 15:38:36.772750\n\n'
revision = 'cefabc8f7d38'
down_revision = '6c7537a6004a'
import sqlalchemy as sa
from alembic import op

def upgrade():
    with op.batch_alter_table('ab_view_menu') as (batch_op):
        batch_op.alter_column('name',
          existing_type=sa.String(length=100),
          existing_nullable=False,
          type_=sa.String(length=255),
          nullable=False)


def downgrade():
    with op.batch_alter_table('ab_view_menu') as (batch_op):
        batch_op.alter_column('name',
          existing_type=sa.String(length=255),
          existing_nullable=False,
          type_=sa.String(length=100),
          nullable=False)