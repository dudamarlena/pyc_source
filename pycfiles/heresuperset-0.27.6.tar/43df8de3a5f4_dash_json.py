# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/43df8de3a5f4_dash_json.py
# Compiled at: 2018-08-15 11:21:52
"""empty message

Revision ID: 43df8de3a5f4
Revises: 7dbf98566af7
Create Date: 2016-01-18 23:43:16.073483

"""
revision = '43df8de3a5f4'
down_revision = '7dbf98566af7'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('dashboards', sa.Column('json_metadata', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('dashboards', 'json_metadata')