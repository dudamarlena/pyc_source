# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpyle/da/docassemble_webapp/docassemble/webapp/alembic/versions/66f71cf543a4_temp_user_id_to_userdictkeys.py
# Compiled at: 2018-05-12 21:02:46
"""temp_user_id_to_userdictkeys

Revision ID: 66f71cf543a4
Revises: 025e06b85efc
Create Date: 2018-05-12 20:59:04.463045

"""
from alembic import op
import sqlalchemy as sa
from docassemble.webapp.database import dbtableprefix
revision = '66f71cf543a4'
down_revision = '025e06b85efc'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(dbtableprefix + 'userdictkeys', sa.Column('temp_user_id', sa.Integer))


def downgrade():
    op.drop_column(dbtableprefix + 'userdictkeys', 'temp_user_id')