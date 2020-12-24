# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\a61b40f9f57f_remove_allow_run_sync.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 1384 bytes
"""remove allow_run_sync

Revision ID: a61b40f9f57f
Revises: 46f444d8b9b7
Create Date: 2018-11-27 11:53:17.512627

"""
from alembic import op
import sqlalchemy as sa
revision = 'a61b40f9f57f'
down_revision = '46f444d8b9b7'

def upgrade():
    with op.batch_alter_table('dbs') as (batch_op):
        batch_op.drop_column('allow_run_sync')


def downgrade():
    op.add_column('dbs', sa.Column('allow_run_sync',
      sa.Integer(display_width=1),
      autoincrement=False,
      nullable=True))