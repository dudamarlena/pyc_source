# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/867bf4f117f9_adding_extra_field_to_database_model.py
# Compiled at: 2019-04-24 13:46:49
# Size of source mod 2**32: 1207 bytes
"""Adding extra field to Database model

Revision ID: 867bf4f117f9
Revises: fee7b758c130
Create Date: 2016-04-03 15:23:20.280841

"""
revision = '867bf4f117f9'
down_revision = 'fee7b758c130'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('dbs', sa.Column('extra', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('dbs', 'extra')