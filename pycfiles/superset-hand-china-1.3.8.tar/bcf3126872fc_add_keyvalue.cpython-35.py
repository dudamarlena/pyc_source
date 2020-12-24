# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ljf/superset/superset18/superset/migrations/versions/bcf3126872fc_add_keyvalue.py
# Compiled at: 2017-10-30 08:27:50
# Size of source mod 2**32: 697 bytes
"""Add keyvalue table

Revision ID: bcf3126872fc
Revises: f18570e03440
Create Date: 2017-01-10 11:47:56.306938

"""
revision = 'bcf3126872fc'
down_revision = 'f18570e03440'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('keyvalue', sa.Column('id', sa.Integer(), nullable=False), sa.Column('value', sa.Text(), nullable=False), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('keyvalue')