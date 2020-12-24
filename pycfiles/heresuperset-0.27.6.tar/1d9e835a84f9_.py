# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/1d9e835a84f9_.py
# Compiled at: 2018-08-15 11:21:52
"""empty message

Revision ID: 1d9e835a84f9
Revises: 3dda56f1c4c6
Create Date: 2018-07-16 18:04:07.764659

"""
revision = '1d9e835a84f9'
down_revision = '3dda56f1c4c6'
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression

def upgrade():
    op.add_column('dbs', sa.Column('allow_csv_upload', sa.Boolean(), nullable=False, server_default=expression.true()))


def downgrade():
    op.drop_column('dbs', 'allow_csv_upload')