# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/322364e7de8b_create_new_tables_for_quest.py
# Compiled at: 2016-09-02 10:29:34
"""Create new tables for Quest

Revision ID: 322364e7de8b
Revises: 508367dcbbb5
Create Date: 2016-09-02 19:59:34.417310

"""
revision = '322364e7de8b'
down_revision = '508367dcbbb5'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('milestone', sa.Column('id', sa.Integer(), nullable=False), sa.Column('position', sa.Integer(), nullable=True), sa.Column('badge_id', sa.Unicode(length=128), nullable=False), sa.Column('series_id', sa.Unicode(length=128), nullable=False), sa.ForeignKeyConstraint(['badge_id'], ['badges.id']), sa.ForeignKeyConstraint(['series_id'], ['series.id']), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('id'), sa.UniqueConstraint('position', 'badge_id', 'series_id'))
    op.drop_table('perk')


def downgrade():
    op.create_table('perk', sa.Column('id', sa.INTEGER(), nullable=False), sa.Column('position', sa.INTEGER(), nullable=True), sa.Column('badge_id', sa.VARCHAR(length=128), nullable=False), sa.Column('series_id', sa.VARCHAR(length=128), nullable=False), sa.ForeignKeyConstraint(['badge_id'], ['badges.id']), sa.ForeignKeyConstraint(['series_id'], ['series.id']), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('id'), sa.UniqueConstraint('position', 'badge_id', 'series_id'))
    op.drop_table('milestone')