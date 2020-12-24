# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxime_beauchemin/code/panoramix/panoramix/migrations/versions/2929af7925ed_tz_offsets_in_data_sources.py
# Compiled at: 2016-02-29 11:08:07
"""TZ offsets in data sources

Revision ID: 2929af7925ed
Revises: 1e2841a4128
Create Date: 2015-10-19 20:54:00.565633

"""
revision = '2929af7925ed'
down_revision = '1e2841a4128'
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('datasources', sa.Column('offset', sa.Integer(), nullable=True))
    op.add_column('tables', sa.Column('offset', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('tables', 'offset')
    op.drop_column('datasources', 'offset')