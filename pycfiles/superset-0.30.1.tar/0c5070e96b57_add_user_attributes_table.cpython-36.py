# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/0c5070e96b57_add_user_attributes_table.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 1937 bytes
"""add user attributes table

Revision ID: 0c5070e96b57
Revises: 7fcdcde0761c
Create Date: 2018-08-06 14:38:18.965248

"""
revision = '0c5070e96b57'
down_revision = '7fcdcde0761c'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.create_table('user_attribute', sa.Column('created_on', (sa.DateTime()), nullable=True), sa.Column('changed_on', (sa.DateTime()), nullable=True), sa.Column('id', (sa.Integer()), nullable=False), sa.Column('user_id', (sa.Integer()), nullable=True), sa.Column('welcome_dashboard_id', (sa.Integer()), nullable=True), sa.Column('created_by_fk', (sa.Integer()), nullable=True), sa.Column('changed_by_fk', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.ForeignKeyConstraint(['welcome_dashboard_id'], ['dashboards.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('user_attribute')