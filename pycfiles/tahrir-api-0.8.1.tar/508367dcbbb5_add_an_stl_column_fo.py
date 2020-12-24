# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/508367dcbbb5_add_an_stl_column_fo.py
# Compiled at: 2016-04-21 17:38:50
"""Add an stl column for badges.

Revision ID: 508367dcbbb5
Revises: 2879ed5a6297
Create Date: 2014-07-11 09:36:33.211281

"""
revision = '508367dcbbb5'
down_revision = '2879ed5a6297'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('badges', sa.Column('stl', sa.Unicode(128)))


def downgrade():
    op.drop_column('badges', 'stl')