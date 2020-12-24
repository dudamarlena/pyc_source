# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/8e80a26a31db_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1685 bytes
"""empty message

Revision ID: 8e80a26a31db
Revises: 2591d77e9831
Create Date: 2016-01-13 20:24:45.256437

"""
revision = '8e80a26a31db'
down_revision = '2591d77e9831'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.create_table('url', sa.Column('created_on', (sa.DateTime()), nullable=False), sa.Column('changed_on', (sa.DateTime()), nullable=False), sa.Column('id', (sa.Integer()), nullable=False), sa.Column('url', (sa.Text()), nullable=True), sa.Column('created_by_fk', (sa.Integer()), nullable=True), sa.Column('changed_by_fk', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('url')