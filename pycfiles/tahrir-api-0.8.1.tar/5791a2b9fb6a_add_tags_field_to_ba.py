# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/5791a2b9fb6a_add_tags_field_to_ba.py
# Compiled at: 2016-04-21 17:38:50
"""Add tags field to badges.

Revision ID: 5791a2b9fb6a
Revises: 39583332f4ea
Create Date: 2013-06-10 13:05:40.130328

"""
revision = '5791a2b9fb6a'
down_revision = '39583332f4ea'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('badges', sa.Column('tags', sa.Text))


def downgrade():
    op.drop_column('badges', 'tags')