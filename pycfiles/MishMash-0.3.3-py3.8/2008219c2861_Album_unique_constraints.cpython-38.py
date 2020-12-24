# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/alembic/versions/2008219c2861_Album_unique_constraints.py
# Compiled at: 2019-12-04 00:39:14
# Size of source mod 2**32: 711 bytes
"""Album unique constraints

Revision ID: 2008219c2861
Revises: 74df8fa5a35f
Create Date: 2019-02-09 20:58:43.822325

"""
from alembic import op
import sqlalchemy as sa
revision = '2008219c2861'
down_revision = '74df8fa5a35f'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('tracks') as (batch_op):
        batch_op.alter_column('metadata_format', existing_type=sa.VARCHAR(length=7), nullable=False)


def downgrade():
    with op.batch_alter_table('tracks') as (batch_op):
        batch_op.alter_column('metadata_format', existing_type=sa.VARCHAR(length=7), nullable=True)