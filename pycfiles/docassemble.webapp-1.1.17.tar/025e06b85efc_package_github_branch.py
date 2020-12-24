# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpyle/da/docassemble_webapp/docassemble/webapp/alembic/versions/025e06b85efc_package_github_branch.py
# Compiled at: 2017-12-01 20:46:58
"""package github branch

Revision ID: 025e06b85efc
Revises: f0b00081fda9
Create Date: 2017-12-01 20:37:28.967575

"""
from alembic import op
import sqlalchemy as sa
from docassemble.webapp.database import dbtableprefix
revision = '025e06b85efc'
down_revision = 'f0b00081fda9'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(dbtableprefix + 'package', sa.Column('gitbranch', sa.String(255)))


def downgrade():
    op.drop_column(dbtableprefix + 'package', 'gitbranch')