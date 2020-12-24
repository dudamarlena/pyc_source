# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ljf/superset/superset18/superset/migrations/versions/43df8de3a5f4_dash_json.py
# Compiled at: 2017-10-30 08:27:50
# Size of source mod 2**32: 430 bytes
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