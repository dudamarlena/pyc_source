# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mawardrop/Repositories/github/knowledge-repo/knowledge_repo/app/migrations/versions/d15f6cac07e1_add_subtitle_field_to_post_database.py
# Compiled at: 2018-10-03 20:30:12
# Size of source mod 2**32: 433 bytes
"""Add subtitle field to post database.

Revision ID: d15f6cac07e1
Revises: 009eafe4838f
Create Date: 2018-10-03 12:31:18.462880

"""
revision = 'd15f6cac07e1'
down_revision = '009eafe4838f'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('posts', sa.Column('subtitle', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('posts', 'subtitle')