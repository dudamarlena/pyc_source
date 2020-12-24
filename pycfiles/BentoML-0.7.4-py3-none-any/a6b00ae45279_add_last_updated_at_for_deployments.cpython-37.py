# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chaoyuyang/workspace/BentoML/bentoml/migrations/versions/a6b00ae45279_add_last_updated_at_for_deployments.py
# Compiled at: 2019-10-24 18:17:34
# Size of source mod 2**32: 474 bytes
"""add last_updated_at for deployments

Revision ID: a6b00ae45279
Revises: 095fb029da39
Create Date: 2019-10-15 15:59:25.742280

"""
from alembic import op
import sqlalchemy as sa
revision = 'a6b00ae45279'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('deployments', sa.Column('last_updated_at', sa.DateTime))


def downgrade():
    op.drop_column('deployments', 'last_updated_at')