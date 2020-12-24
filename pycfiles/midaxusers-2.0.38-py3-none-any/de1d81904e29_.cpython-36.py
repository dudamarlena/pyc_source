# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\usersapi\midaxusersutils\migrations\versions\de1d81904e29_.py
# Compiled at: 2018-11-21 09:52:10
# Size of source mod 2**32: 964 bytes
"""empty message

Revision ID: de1d81904e29
Revises: 427f14007618
Create Date: 2018-11-21 16:52:09.978808

"""
from alembic import op
import sqlalchemy as sa, midaxusers.migration_types
revision = 'de1d81904e29'
down_revision = '427f14007618'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('USERS', sa.Column('manage_domain_users', sa.Boolean(name='bl_U_man_dom_usrs'), server_default=(sa.text('0')), nullable=True))
    op.add_column('USERS', sa.Column('manage_subdomain_users', sa.Boolean(name='bl_U_man_sdom_usrs'), server_default=(sa.text('1')), nullable=True))


def downgrade():
    op.drop_column('USERS', 'manage_subdomain_users')
    op.drop_column('USERS', 'manage_domain_users')