# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vandercf/git/atramhasis/atramhasis/alembic/versions/3bcf11802900_add_markup_to_source.py
# Compiled at: 2017-06-22 05:19:07
"""Add markup to source.

Revision ID: 3bcf11802900
Revises: 1a4d62b02630
Create Date: 2016-05-25 14:31:51.579412

"""
revision = '3bcf11802900'
down_revision = '1a4d62b02630'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('source', sa.Column('markup', sa.String(20)))


def downgrade():
    op.drop_column('source', 'markup')