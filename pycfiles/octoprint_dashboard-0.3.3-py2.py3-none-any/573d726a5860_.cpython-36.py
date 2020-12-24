# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jirimakarius/Projects/OctoPrint-Dashboard/octoprint_dashboard/model/migrations/versions/573d726a5860_.py
# Compiled at: 2017-10-19 04:30:20
# Size of source mod 2**32: 2646 bytes
"""empty message

Revision ID: 573d726a5860
Revises: 
Create Date: 2017-10-19 10:08:55.047665

"""
from alembic import op
import sqlalchemy as sa
revision = '573d726a5860'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('config', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('secret', sa.String(length=80), nullable=True), sa.Column('oauth_client_id', (sa.String()), nullable=True), sa.Column('oauth_client_secret', (sa.String()), nullable=True), sa.Column('oauth_redirect_uri', (sa.String()), nullable=True), sa.PrimaryKeyConstraint('id'))
    op.create_table('group', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('name', sa.String(length=80), nullable=True), sa.PrimaryKeyConstraint('id'))
    op.create_table('printer', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('name', sa.String(length=80), nullable=True), sa.Column('apikey', sa.String(length=80), nullable=True), sa.Column('url', sa.String(length=80), nullable=True), sa.PrimaryKeyConstraint('id'))
    op.create_table('user', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('username', sa.String(length=80), nullable=True), sa.Column('access_token', sa.String(length=80), nullable=True), sa.Column('refresh_token', sa.String(length=80), nullable=True), sa.Column('superadmin', (sa.Boolean()), nullable=True), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('username'))
    op.create_table('group_user', sa.Column('group_id', (sa.Integer()), nullable=False), sa.Column('user_id', (sa.Integer()), nullable=False), sa.Column('role', sa.String(length=80), nullable=False, server_default='user'), sa.ForeignKeyConstraint(['group_id'], ['group.id']), sa.ForeignKeyConstraint(['user_id'], ['user.id']), sa.PrimaryKeyConstraint('group_id', 'user_id'))
    op.create_table('printer_group', sa.Column('printer_id', (sa.Integer()), nullable=True), sa.Column('group_id', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['group_id'], ['group.id']), sa.ForeignKeyConstraint(['printer_id'], ['printer.id']))


def downgrade():
    op.drop_table('printer_group')
    op.drop_table('group_user')
    op.drop_table('user')
    op.drop_table('printer')
    op.drop_table('group')
    op.drop_table('config')