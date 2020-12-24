# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\usersapi\midaxusersutils\migrations\versions\f3806782e4b8_.py
# Compiled at: 2018-11-21 13:24:52
# Size of source mod 2**32: 788 bytes
"""empty message

Revision ID: f3806782e4b8
Revises: de1d81904e29
Create Date: 2018-11-21 19:55:21.696316

"""
from alembic import op
import sqlalchemy as sa, midaxusers.migration_types
revision = 'f3806782e4b8'
down_revision = '427f14007618'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('USERS', sa.Column('user_manage_rights', sa.Enum('none', 'subdomain', 'domain', name='managertypesenum'), server_default='subdomain', nullable=False))


def downgrade():
    op.drop_column('USERS', 'user_manage_rights')