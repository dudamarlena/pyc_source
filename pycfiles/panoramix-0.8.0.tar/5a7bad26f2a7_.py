# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxime_beauchemin/code/panoramix/panoramix/migrations/versions/5a7bad26f2a7_.py
# Compiled at: 2016-02-29 11:08:07
"""empty message

Revision ID: 5a7bad26f2a7
Revises: 4e6a06bad7a8
Create Date: 2015-10-05 10:32:15.850753

"""
revision = '5a7bad26f2a7'
down_revision = '4e6a06bad7a8'
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('dashboards', sa.Column('css', sa.Text(), nullable=True))
    op.add_column('dashboards', sa.Column('description', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('dashboards', 'description')
    op.drop_column('dashboards', 'css')