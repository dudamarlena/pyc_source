# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\2591d77e9831_user_id.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 1426 bytes
"""user_id

Revision ID: 2591d77e9831
Revises: 12d55656cbca
Create Date: 2015-12-15 17:02:45.128709

"""
revision = '2591d77e9831'
down_revision = '12d55656cbca'
from alembic import op
import sqlalchemy as sa

def upgrade():
    with op.batch_alter_table('tables') as (batch_op):
        batch_op.add_column(sa.Column('user_id', sa.Integer()))
        batch_op.create_foreign_key('user_id', 'ab_user', ['user_id'], ['id'])


def downgrade():
    with op.batch_alter_table('tables') as (batch_op):
        batch_op.drop_constraint('user_id', type_='foreignkey')
        batch_op.drop_column('user_id')