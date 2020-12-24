# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: alembic/versions/3876f3c32a4a_.py
# Compiled at: 2013-03-19 22:52:41
"""empty message

Revision ID: 3876f3c32a4a
Revises: None
Create Date: 2012-10-13 03:53:18.924283

"""
revision = '3876f3c32a4a'
down_revision = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('worklog', sa.Column('id', sa.Integer(), nullable=False), sa.Column('activity', sa.Enum('start', 'end', 'resume'), nullable=True), sa.Column('description', sa.String(length=256), nullable=True), sa.Column('created_at', sa.DateTime(), nullable=True), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('worklog')