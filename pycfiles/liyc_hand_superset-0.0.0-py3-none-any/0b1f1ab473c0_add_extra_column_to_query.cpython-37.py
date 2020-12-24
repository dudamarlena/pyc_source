# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\0b1f1ab473c0_add_extra_column_to_query.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 1316 bytes
"""Add extra column to Query

Revision ID: 0b1f1ab473c0
Revises: 55e910a74826
Create Date: 2018-11-05 08:42:56.181012

"""
from alembic import op
import sqlalchemy as sa
revision = '0b1f1ab473c0'
down_revision = '55e910a74826'

def upgrade():
    with op.batch_alter_table('query') as (batch_op):
        batch_op.add_column(sa.Column('extra_json', (sa.Text()), nullable=True))


def downgrade():
    with op.batch_alter_table('query') as (batch_op):
        batch_op.drop_column('extra_json')