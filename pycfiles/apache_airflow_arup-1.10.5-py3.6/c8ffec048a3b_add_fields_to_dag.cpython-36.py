# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/c8ffec048a3b_add_fields_to_dag.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1367 bytes
"""add fields to dag

Revision ID: c8ffec048a3b
Revises: 41f5f12752f8
Create Date: 2018-12-23 21:55:46.463634

"""
from alembic import op
import sqlalchemy as sa
revision = 'c8ffec048a3b'
down_revision = '41f5f12752f8'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('dag', sa.Column('description', (sa.Text()), nullable=True))
    op.add_column('dag', sa.Column('default_view', (sa.String(25)), nullable=True))


def downgrade():
    op.drop_column('dag', 'description')
    op.drop_column('dag', 'default_view')