# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\7dbf98566af7_slice_description.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 1203 bytes
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
    op.add_column('slices', sa.Column('description', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('slices', 'description')