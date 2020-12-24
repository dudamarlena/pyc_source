# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\usersapi\midaxusersutils\migrations\versions\95a6db51f87c_.py
# Compiled at: 2018-11-21 12:51:40
# Size of source mod 2**32: 759 bytes
"""empty message

Revision ID: 95a6db51f87c
Revises: de1d81904e29
Create Date: 2018-11-21 19:51:40.744316

"""
from alembic import op
import sqlalchemy as sa, midaxusers.migration_types
revision = '95a6db51f87c'
down_revision = 'de1d81904e29'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('USERS', sa.Column('user_manage_rights', sa.Enum('none', 'subdomain', 'domain', name='managertypesenum'), nullable=True))


def downgrade():
    op.drop_column('USERS', 'user_manage_rights')