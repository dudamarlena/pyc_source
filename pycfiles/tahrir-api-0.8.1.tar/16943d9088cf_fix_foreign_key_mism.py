# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/16943d9088cf_fix_foreign_key_mism.py
# Compiled at: 2016-04-21 17:38:50
"""fix foreign key mismatch

Revision ID: 16943d9088cf
Revises: 24282792d72a
Create Date: 2013-06-23 22:55:47.775736

"""
revision = '16943d9088cf'
down_revision = '24282792d72a'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.alter_column('invitations', 'created_by', type_=sa.Integer)


def downgrade():
    op.alter_column('invitations', 'created_by', type_=sa.Unicode(128))