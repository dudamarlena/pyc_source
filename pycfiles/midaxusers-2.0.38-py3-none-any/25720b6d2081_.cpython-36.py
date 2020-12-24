# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\usersapi\migrations\versions\25720b6d2081_.py
# Compiled at: 2018-07-26 13:38:39
# Size of source mod 2**32: 2527 bytes
"""empty message

Revision ID: 25720b6d2081
Revises: 
Create Date: 2018-07-26 20:38:39.631257

"""
from alembic import op
import sqlalchemy as sa, midaxusers.migration_types
revision = '25720b6d2081'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('USERS', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('uuid', (midaxusers.migration_types.HybridUniqueIdentifier()), nullable=True), sa.Column('domain', sa.String(length=64), nullable=True), sa.Column('username', sa.String(length=64), nullable=True), sa.Column('email', sa.String(length=120), nullable=True), sa.Column('role', (sa.Integer()), nullable=True), sa.Column('password_hash', sa.String(length=256), nullable=True), sa.Column('force_password_change', (sa.Boolean()), server_default=(sa.text('0')), nullable=True), sa.Column('active', (sa.Boolean()), server_default=(sa.text('1')), nullable=True), sa.Column('time_updated', sa.DateTime(timezone=True), server_default=(sa.text('CURRENT_TIMESTAMP')), nullable=True), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('domain', 'username', name='domain_user_uq'))
    op.create_index((op.f('ix_USERS_domain')), 'USERS', ['domain'], unique=False)
    op.create_index((op.f('ix_USERS_email')), 'USERS', ['email'], unique=True)
    op.create_index((op.f('ix_USERS_username')), 'USERS', ['username'], unique=False)
    op.create_index((op.f('ix_USERS_uuid')), 'USERS', ['uuid'], unique=True)
    op.create_table('USER_ATTRIBUTES', sa.Column('user_uuid', (midaxusers.migration_types.HybridUniqueIdentifier()), nullable=False), sa.Column('name', sa.String(length=64), nullable=False), sa.Column('value', sa.String(length=64), nullable=True), sa.Column('time_updated', sa.DateTime(timezone=True), server_default=(sa.text('CURRENT_TIMESTAMP')), nullable=True), sa.PrimaryKeyConstraint('user_uuid', 'name', name='userattributes_pk'))


def downgrade():
    op.drop_table('USER_ATTRIBUTES')
    op.drop_index((op.f('ix_USERS_uuid')), table_name='USERS')
    op.drop_index((op.f('ix_USERS_username')), table_name='USERS')
    op.drop_index((op.f('ix_USERS_email')), table_name='USERS')
    op.drop_index((op.f('ix_USERS_domain')), table_name='USERS')
    op.drop_table('USERS')