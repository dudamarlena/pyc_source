# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /repos/dagobah/dagobah/backend/migrations/versions/2ab7af991b87_v0_2.py
# Compiled at: 2014-08-17 14:29:16
"""v0.2

Revision ID: 2ab7af991b87
Revises: None
Create Date: 2013-09-04 22:14:28.552136

"""
revision = '2ab7af991b87'
down_revision = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('dagobah_task', sa.Column('hard_timeout', sa.Integer(), nullable=False, server_default=sa.text('0')))
    op.add_column('dagobah_task', sa.Column('soft_timeout', sa.Integer(), nullable=False, server_default=sa.text('0')))


def downgrade():
    op.drop_column('dagobah_task', 'soft_timeout')
    op.drop_column('dagobah_task', 'hard_timeout')