# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\30bb17c0dc76_.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 1319 bytes
"""empty message

Revision ID: 30bb17c0dc76
Revises: f231d82b9b26
Create Date: 2018-04-08 07:34:12.149910

"""
revision = '30bb17c0dc76'
down_revision = 'f231d82b9b26'
from datetime import date
from alembic import op
import sqlalchemy as sa

def upgrade():
    with op.batch_alter_table('logs') as (batch_op):
        batch_op.drop_column('dt')


def downgrade():
    with op.batch_alter_table('logs') as (batch_op):
        batch_op.add_column(sa.Column('dt', (sa.Date), default=(date.today())))