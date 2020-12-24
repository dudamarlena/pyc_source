# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpyle/da/docassemble_webapp/docassemble/webapp/alembic/versions/eb61567ea005_length_of_subdivisionfirst.py
# Compiled at: 2018-05-15 22:31:37
"""length_of_subdivisionfirst

Revision ID: eb61567ea005
Revises: 66f71cf543a4
Create Date: 2018-05-15 22:24:27.212164

"""
from alembic import op
import sqlalchemy as sa
from docassemble.webapp.database import dbtableprefix
revision = 'eb61567ea005'
down_revision = '66f71cf543a4'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column(dbtableprefix + 'user', 'subdivisionfirst', existing_type=sa.String(length=3), type_=sa.String(length=255), existing_nullable=True)
    op.alter_column(dbtableprefix + 'user', 'country', existing_type=sa.String(length=2), type_=sa.String(length=3), existing_nullable=True)


def downgrade():
    op.alter_column(dbtableprefix + 'user', 'subdivisionfirst', existing_type=sa.String(length=255), type_=sa.String(length=3), existing_nullable=True)
    op.alter_column(dbtableprefix + 'user', 'country', existing_type=sa.String(length=3), type_=sa.String(length=2), existing_nullable=True)