# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ljf/superset/superset18/superset/migrations/versions/a2d606a761d9_adding_favstar_model.py
# Compiled at: 2017-10-30 08:27:50
# Size of source mod 2**32: 768 bytes
"""adding favstar model

Revision ID: a2d606a761d9
Revises: 430039611635
Create Date: 2016-03-13 09:56:58.329512

"""
revision = 'a2d606a761d9'
down_revision = '18e88e1cc004'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('favstar', sa.Column('id', sa.Integer(), nullable=False), sa.Column('user_id', sa.Integer(), nullable=True), sa.Column('class_name', sa.String(length=50), nullable=True), sa.Column('obj_id', sa.Integer(), nullable=True), sa.Column('dttm', sa.DateTime(), nullable=True), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('favstar')