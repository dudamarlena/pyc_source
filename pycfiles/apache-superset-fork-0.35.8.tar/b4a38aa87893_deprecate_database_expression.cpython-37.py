# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/b4a38aa87893_deprecate_database_expression.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1345 bytes
"""deprecate database expression

Revision ID: b4a38aa87893
Revises: ab8c66efdd01
Create Date: 2019-06-05 11:35:16.222519

"""
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