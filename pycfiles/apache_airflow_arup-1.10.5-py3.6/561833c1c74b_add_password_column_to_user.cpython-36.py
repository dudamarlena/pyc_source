# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/561833c1c74b_add_password_column_to_user.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1262 bytes
"""add password column to user

Revision ID: 561833c1c74b
Revises: 40e67319e3a9
Create Date: 2015-11-30 06:51:25.872557

"""
from alembic import op
import sqlalchemy as sa
revision = '561833c1c74b'
down_revision = '40e67319e3a9'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('user', sa.Column('password', sa.String(255)))


def downgrade():
    op.drop_column('user', 'password')