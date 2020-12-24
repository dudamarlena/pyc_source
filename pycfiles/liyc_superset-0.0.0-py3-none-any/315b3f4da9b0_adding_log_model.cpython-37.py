# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\315b3f4da9b0_adding_log_model.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 1543 bytes
"""adding log model

Revision ID: 315b3f4da9b0
Revises: 1a48a5411020
Create Date: 2015-12-04 11:16:58.226984

"""
revision = '315b3f4da9b0'
down_revision = '1a48a5411020'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('logs', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('action', sa.String(length=512), nullable=True), sa.Column('user_id', (sa.Integer()), nullable=True), sa.Column('json', (sa.Text()), nullable=True), sa.Column('dttm', (sa.DateTime()), nullable=True), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('logs')