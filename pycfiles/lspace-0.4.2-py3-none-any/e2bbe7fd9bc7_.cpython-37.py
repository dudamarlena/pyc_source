# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/meatpuppet/dev/lspace/lspace/migrations/versions/e2bbe7fd9bc7_.py
# Compiled at: 2019-06-14 04:37:11
# Size of source mod 2**32: 917 bytes
"""empty message

Revision ID: e2bbe7fd9bc7
Revises: b142d6d9e8da
Create Date: 2019-05-20 23:22:16.784309

"""
from alembic import op
import sqlalchemy as sa
revision = 'e2bbe7fd9bc7'
down_revision = 'b142d6d9e8da'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('meta_cache', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('isbn', sa.String(length=13), nullable=True), sa.Column('service', sa.String(length=10), nullable=True), sa.Column('date', (sa.DateTime()), nullable=True), sa.Column('data', (sa.Text()), nullable=True), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('meta_cache')