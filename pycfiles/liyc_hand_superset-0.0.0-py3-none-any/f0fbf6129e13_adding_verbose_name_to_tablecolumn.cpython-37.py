# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\f0fbf6129e13_adding_verbose_name_to_tablecolumn.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 1276 bytes
"""Adding verbose_name to tablecolumn

Revision ID: f0fbf6129e13
Revises: c3a8f8611885
Create Date: 2016-05-01 12:21:18.331191

"""
revision = 'f0fbf6129e13'
down_revision = 'c3a8f8611885'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('table_columns', sa.Column('verbose_name', sa.String(length=1024), nullable=True))


def downgrade():
    op.drop_column('table_columns', 'verbose_name')