# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\usersapi\midaxusersutils\migrations\versions\e7dd5d1c9592_.py
# Compiled at: 2018-10-22 11:11:33
# Size of source mod 2**32: 851 bytes
"""empty message

Revision ID: e7dd5d1c9592
Revises: 35e79bfb4edd
Create Date: 2018-10-22 18:11:33.934671

"""
from alembic import op
import sqlalchemy as sa, midaxusers.migration_types
from sqlalchemy.dialects import mssql
revision = 'e7dd5d1c9592'
down_revision = '35e79bfb4edd'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('USERS', 'uuid', existing_type=(mssql.UNIQUEIDENTIFIER()),
      nullable=False)


def downgrade():
    op.alter_column('USERS', 'uuid', existing_type=(mssql.UNIQUEIDENTIFIER()),
      nullable=True)