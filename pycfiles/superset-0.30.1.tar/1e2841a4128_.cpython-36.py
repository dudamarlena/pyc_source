# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/1e2841a4128_.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 1213 bytes
"""empty message

Revision ID: 1e2841a4128
Revises: 5a7bad26f2a7
Create Date: 2015-10-05 22:11:00.537054

"""
revision = '1e2841a4128'
down_revision = '5a7bad26f2a7'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('table_columns', sa.Column('expression', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('table_columns', 'expression')