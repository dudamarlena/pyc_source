# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpyle/da/docassemble_webapp/docassemble/webapp/alembic/versions/77e8971ffcbf_first_alembic_revision.py
# Compiled at: 2017-08-21 07:36:02
"""first alembic revision

Revision ID: 77e8971ffcbf
Revises: 
Create Date: 2017-08-13 09:07:33.368044

"""
from alembic import op
import sqlalchemy as sa
from docassemble.webapp.database import dbtableprefix
revision = '77e8971ffcbf'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(dbtableprefix + 'user', sa.Column('modified_at', sa.DateTime))


def downgrade():
    op.drop_column(dbtableprefix + 'user', 'modified_at')