# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/7dbf98566af7_slice_description.py
# Compiled at: 2018-08-15 11:21:52
"""empty message

Revision ID: 7dbf98566af7
Revises: 8e80a26a31db
Create Date: 2016-01-17 22:00:23.640788

"""
revision = '7dbf98566af7'
down_revision = '8e80a26a31db'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('slices', sa.Column('description', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('slices', 'description')