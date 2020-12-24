# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stephenmoore/Projects/utility/photons-interactor/photons_interactor/database/migrations/versions/119f5f1434f7_add_scenes.py
# Compiled at: 2020-02-25 22:11:59
# Size of source mod 2**32: 1212 bytes
"""add_scenes

Revision ID: 119f5f1434f7
Revises: 
Create Date: 2018-07-28 12:12:32.114158

"""
revision = '119f5f1434f7'
down_revision = None
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('scene', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('uuid', sa.String(length=64), nullable=True), sa.Column('matcher', (sa.Text()), nullable=False), sa.Column('power', (sa.Boolean()), nullable=True), sa.Column('color', (sa.Text()), nullable=True), sa.Column('zones', (sa.Text()), nullable=True), sa.Column('chain', (sa.Text()), nullable=True), sa.Column('duration', (sa.Integer()), nullable=True), sa.PrimaryKeyConstraint('id'))
    op.create_index((op.f('ix_scene_uuid')), 'scene', ['uuid'], unique=False)


def downgrade():
    op.drop_index((op.f('ix_scene_uuid')), table_name='scene')
    op.drop_table('scene')