# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpyle/da/docassemble_webapp/docassemble/webapp/alembic/versions/4328f2c08f05_add_indexes.py
# Compiled at: 2019-02-05 19:23:02
"""add indexes

Revision ID: 4328f2c08f05
Revises: eb61567ea005
Create Date: 2019-02-05 19:23:02.744161

"""
from alembic import op
import sqlalchemy as sa
from docassemble.webapp.database import dbtableprefix
revision = '4328f2c08f05'
down_revision = 'eb61567ea005'
branch_labels = None
depends_on = None

def upgrade():
    pass


def downgrade():
    pass