# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/420c02357a1b_add_created_on_field.py
# Compiled at: 2016-04-21 17:38:50
"""Add created_on field to badges table.

Revision ID: 420c02357a1b
Revises: None
Create Date: 2013-06-09 22:23:32.519635

"""
revision = '420c02357a1b'
down_revision = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('badges', sa.Column('created_on', sa.DateTime, nullable=False))


def downgrade():
    op.drop_column('badges', 'created_on')