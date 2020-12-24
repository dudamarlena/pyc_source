# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mawardrop/Repositories/github/knowledge-repo/knowledge_repo/app/migrations/versions/36baffc5df12_add_groups_permissions_to_posts.py
# Compiled at: 2018-03-27 00:36:21
"""Add groups + permissions to posts

Revision ID: 36baffc5df12
Revises: 1b385158fd32
Create Date: 2016-11-02 15:37:12.808143

"""
revision = '36baffc5df12'
down_revision = '1b385158fd32'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('groups', sa.Column('id', sa.Integer(), nullable=False), sa.Column('name', sa.String(length=128), nullable=True), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('name'))
    op.create_table('assoc_group_user', sa.Column('group_id', sa.Integer(), nullable=True), sa.Column('user_id', sa.Integer(), nullable=True), sa.ForeignKeyConstraint(['group_id'], ['groups.id']), sa.ForeignKeyConstraint(['user_id'], ['users.id']))
    op.create_table('assoc_post_group', sa.Column('post_id', sa.Integer(), nullable=True), sa.Column('group_id', sa.Integer(), nullable=True), sa.ForeignKeyConstraint(['group_id'], ['groups.id']), sa.ForeignKeyConstraint(['post_id'], ['posts.id']))
    op.add_column('posts', sa.Column('private', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('posts', 'private')
    op.drop_table('assoc_post_group')
    op.drop_table('assoc_group_user')
    op.drop_table('groups')