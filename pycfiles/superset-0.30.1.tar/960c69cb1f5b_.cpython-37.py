# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/960c69cb1f5b_.py
# Compiled at: 2019-04-24 13:46:49
# Size of source mod 2**32: 1443 bytes
"""add dttm_format related fields in table_columns

Revision ID: 960c69cb1f5b
Revises: d8bc074f7aad
Create Date: 2016-06-16 14:15:19.573183

"""
revision = '960c69cb1f5b'
down_revision = '27ae655e4247'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('table_columns', sa.Column('python_date_format', sa.String(length=255), nullable=True))
    op.add_column('table_columns', sa.Column('database_expression', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('table_columns', 'python_date_format')
    op.drop_column('table_columns', 'database_expression')