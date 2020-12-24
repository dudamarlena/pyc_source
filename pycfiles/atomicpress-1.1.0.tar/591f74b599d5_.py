# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martinsandstrom/Projekt/github/atomicpress/atomicpress/migrations/versions/591f74b599d5_.py
# Compiled at: 2016-05-08 15:39:28
"""empty message

Revision ID: 591f74b599d5
Revises: 1a8ee645def6
Create Date: 2016-05-08 21:20:38.759813

"""
revision = '591f74b599d5'
down_revision = '1a8ee645def6'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('post', sa.Column('template', sa.String(255)))


def downgrade():
    op.drop_column('post', 'template')