# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/4fa88fe24e94_owners_many_to_many.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1940 bytes
"""owners_many_to_many

Revision ID: 4fa88fe24e94
Revises: b4456560d4f3
Create Date: 2016-04-15 17:58:33.842012

"""
revision = '4fa88fe24e94'
down_revision = 'b4456560d4f3'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.create_table('dashboard_user', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('user_id', (sa.Integer()), nullable=True), sa.Column('dashboard_id', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['dashboard_id'], ['dashboards.id']), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))
    op.create_table('slice_user', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('user_id', (sa.Integer()), nullable=True), sa.Column('slice_id', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['slice_id'], ['slices.id']), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('slice_user')
    op.drop_table('dashboard_user')