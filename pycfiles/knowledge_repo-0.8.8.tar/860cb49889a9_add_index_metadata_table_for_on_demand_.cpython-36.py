# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mawardrop/Repositories/github/knowledge-repo/knowledge_repo/app/migrations/versions/860cb49889a9_add_index_metadata_table_for_on_demand_.py
# Compiled at: 2018-03-27 00:36:21
# Size of source mod 2**32: 804 bytes
"""Add index metadata table for on-demand reindexing.

Revision ID: 860cb49889a9
Revises: 36baffc5df12
Create Date: 2016-11-08 00:56:21.810049

"""
revision = '860cb49889a9'
down_revision = '36baffc5df12'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('index_metadata', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('type', sa.String(length=255), nullable=False), sa.Column('name', sa.String(length=512), nullable=False), sa.Column('value', sa.String(length=512), nullable=True), sa.Column('updated_at', (sa.DateTime()), nullable=True), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('type', 'name', name='_uc_type_name'))


def downgrade():
    op.drop_table('index_metadata')