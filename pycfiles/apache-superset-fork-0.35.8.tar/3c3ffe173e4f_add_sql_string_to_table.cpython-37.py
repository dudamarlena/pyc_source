# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/3c3ffe173e4f_add_sql_string_to_table.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1197 bytes
"""add_sql_string_to_table

Revision ID: 3c3ffe173e4f
Revises: ad82a75afd82
Create Date: 2016-08-18 14:06:28.784699

"""
revision = '3c3ffe173e4f'
down_revision = 'ad82a75afd82'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('tables', sa.Column('sql', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('tables', 'sql')