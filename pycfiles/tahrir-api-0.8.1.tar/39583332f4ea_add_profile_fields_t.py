# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/39583332f4ea_add_profile_fields_t.py
# Compiled at: 2016-04-21 17:38:50
"""Add profile fields to persons.

Revision ID: 39583332f4ea
Revises: fa1d309e8c3
Create Date: 2013-06-10 12:33:45.319780

"""
revision = '39583332f4ea'
down_revision = 'fa1d309e8c3'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('persons', sa.Column('nickname', sa.Text))
    op.add_column('persons', sa.Column('website', sa.Text))
    op.add_column('persons', sa.Column('bio', sa.Text))


def downgrade():
    op.drop_column('persons', 'nickname')
    op.drop_column('persons', 'website')
    op.drop_column('persons', 'bio')