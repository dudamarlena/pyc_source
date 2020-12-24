# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ljf/superset/superset18/superset/migrations/versions/bb51420eaf83_add_schema_to_table_model.py
# Compiled at: 2017-10-30 08:27:50
# Size of source mod 2**32: 432 bytes
"""add schema to table model

Revision ID: bb51420eaf83
Revises: 867bf4f117f9
Create Date: 2016-04-11 22:41:06.185955

"""
revision = 'bb51420eaf83'
down_revision = '867bf4f117f9'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('tables', sa.Column('schema', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('tables', 'schema')