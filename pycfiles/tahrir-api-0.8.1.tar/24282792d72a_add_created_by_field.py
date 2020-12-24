# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/24282792d72a_add_created_by_field.py
# Compiled at: 2016-04-21 17:38:50
"""Add created_by field to invitations.

Revision ID: 24282792d72a
Revises: 5791a2b9fb6a
Create Date: 2013-06-10 15:51:02.288685

"""
revision = '24282792d72a'
down_revision = '5791a2b9fb6a'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('invitations', sa.Column('created_by', sa.Unicode(128), sa.ForeignKey('persons.id'), nullable=False))


def downgrade():
    op.drop_column('invitations', 'created_by')