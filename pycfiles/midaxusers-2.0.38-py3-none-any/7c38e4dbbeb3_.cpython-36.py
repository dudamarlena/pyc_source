# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\usersapi\midaxusersutils\migrations\versions\7c38e4dbbeb3_.py
# Compiled at: 2018-10-30 15:06:39
# Size of source mod 2**32: 1585 bytes
"""empty message

Revision ID: 7c38e4dbbeb3
Revises: 43a3450ebe27
Create Date: 2018-10-30 21:01:14.592773

"""
from alembic import op
import sqlalchemy as sa, midaxusers.migration_types
revision = '7c38e4dbbeb3'
down_revision = '43a3450ebe27'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('USER_ATTRIBUTES') as (batch_op):
        batch_op.drop_constraint('USER_ATTRIBUTES_user_uuid_fkey',
          type_='foreignkey')
    op.create_foreign_key('USER_ATTRIBUTES_user_uuid_fkey',
      'USER_ATTRIBUTES', 'USERS', [
     'user_uuid'],
      ['uuid'], ondelete='CASCADE', onupdate='CASCADE')
    with op.batch_alter_table('USER_LOGINS') as (batch_op):
        batch_op.drop_constraint('USER_LOGINS_user_uuid_fkey',
          type_='foreignkey')
    op.create_foreign_key('USER_LOGINS_user_uuid_fkey',
      'USER_LOGINS', 'USERS', [
     'user_uuid'],
      ['uuid'], ondelete='CASCADE', onupdate='CASCADE')


def downgrade():
    with op.batch_alter_table('USER_ATTRIBUTES') as (batch_op):
        batch_op.drop_constraint('USER_ATTRIBUTES_user_uuid_fkey',
          type_='foreignkey')
    op.create_foreign_key('USER_ATTRIBUTES_user_uuid_fkey', 'USER_ATTRIBUTES', 'USERS', [
     'user_uuid'], ['uuid'])
    with op.batch_alter_table('USER_LOGINS') as (batch_op):
        batch_op.drop_constraint('USER_LOGINS_user_uuid_fkey',
          type_='foreignkey')
    op.create_foreign_key('USER_LOGINS_user_uuid_fkey', 'USER_LOGINS', 'USERS', [
     'user_uuid'], ['uuid'])