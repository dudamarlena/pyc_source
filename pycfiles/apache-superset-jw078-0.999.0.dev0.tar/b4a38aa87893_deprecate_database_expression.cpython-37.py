# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/b4a38aa87893_deprecate_database_expression.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1345 bytes
__doc__ = 'deprecate database expression\n\nRevision ID: b4a38aa87893\nRevises: ab8c66efdd01\nCreate Date: 2019-06-05 11:35:16.222519\n\n'
revision = 'b4a38aa87893'
down_revision = 'ab8c66efdd01'
import sqlalchemy as sa
from alembic import op

def upgrade():
    with op.batch_alter_table('table_columns') as (batch_op):
        batch_op.drop_column('database_expression')


def downgrade():
    with op.batch_alter_table('table_columns') as (batch_op):
        batch_op.add_column(sa.Column('database_expression', sa.String(255)))