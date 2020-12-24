# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/41f5f12752f8_add_superuser_field.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1247 bytes
"""add superuser field

Revision ID: 41f5f12752f8
Revises: 03bc53e68815
Create Date: 2018-12-04 15:50:04.456875

"""
from alembic import op
import sqlalchemy as sa
revision = '41f5f12752f8'
down_revision = '03bc53e68815'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('superuser', (sa.Boolean()), default=False))


def downgrade():
    op.drop_column('users', 'superuser')