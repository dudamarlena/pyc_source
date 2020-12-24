# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/55e910a74826_add_metadata_column_to_annotation_model_.py
# Compiled at: 2019-04-24 13:46:49
# Size of source mod 2**32: 1244 bytes
"""add_metadata_column_to_annotation_model.py

Revision ID: 55e910a74826
Revises: 1a1d627ebd8e
Create Date: 2018-08-29 14:35:20.407743

"""
revision = '55e910a74826'
down_revision = '1a1d627ebd8e'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('annotation', sa.Column('json_metadata', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('annotation', 'json_metadata')