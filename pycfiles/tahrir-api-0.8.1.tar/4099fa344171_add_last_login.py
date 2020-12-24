# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/4099fa344171_add_last_login.py
# Compiled at: 2016-04-21 17:38:50
"""add last login

Revision ID: 4099fa344171
Revises: 139ec7ed17b7
Create Date: 2013-10-24 10:13:45.104902

"""
revision = '4099fa344171'
down_revision = '139ec7ed17b7'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('persons', sa.Column('last_login', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('persons', 'last_login')