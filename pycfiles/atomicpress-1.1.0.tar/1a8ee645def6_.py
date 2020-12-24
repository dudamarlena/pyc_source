# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martinsandstrom/Projekt/github/atomicpress/atomicpress/migrations/versions/1a8ee645def6_.py
# Compiled at: 2016-05-08 15:39:20
"""Added category and tag fields

Revision ID: 1a8ee645def6
Revises: 127682c11a74
Create Date: 2014-09-28 18:41:13.168379

"""
revision = '1a8ee645def6'
down_revision = '127682c11a74'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('post', sa.Column('category', sa.Boolean(), nullable=True))
    op.add_column('post', sa.Column('tag', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('post', 'tag')
    op.drop_column('post', 'category')