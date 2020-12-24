# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/139ec7ed17b7_add_a_rank_column_to.py
# Compiled at: 2016-04-21 17:38:50
"""Add a rank column to the Person table.

Revision ID: 139ec7ed17b7
Revises: 3c7fd5b4e2c2
Create Date: 2013-08-16 12:06:00.092052

"""
revision = '139ec7ed17b7'
down_revision = '3c7fd5b4e2c2'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('persons', sa.Column('rank', sa.Integer, default=None))
    return


def downgrade():
    op.drop_column('persons', 'rank')