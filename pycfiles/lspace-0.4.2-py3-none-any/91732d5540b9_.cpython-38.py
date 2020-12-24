# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/meatpuppet/code/lspace/lspace/migrations/versions/91732d5540b9_.py
# Compiled at: 2019-06-14 04:37:11
# Size of source mod 2**32: 676 bytes
"""empty message

Revision ID: 91732d5540b9
Revises: e2bbe7fd9bc7
Create Date: 2019-06-06 22:52:21.057872

"""
from alembic import op
import sqlalchemy as sa
revision = '91732d5540b9'
down_revision = 'e2bbe7fd9bc7'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('books', sa.Column('metadata_source', sa.String(length=20), nullable=True))


def downgrade():
    op.drop_column('books', 'metadata_source')