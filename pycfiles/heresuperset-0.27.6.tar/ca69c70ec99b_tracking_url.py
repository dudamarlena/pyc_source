# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/ca69c70ec99b_tracking_url.py
# Compiled at: 2018-08-15 11:21:52
"""tracking_url

Revision ID: ca69c70ec99b
Revises: a65458420354
Create Date: 2017-07-26 20:09:52.606416

"""
revision = 'ca69c70ec99b'
down_revision = 'a65458420354'
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('query', sa.Column('tracking_url', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('query', 'tracking_url')