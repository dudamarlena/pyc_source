# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stephenmoore/Projects/utility/photons-interactor/photons_interactor/database/migrations/versions/f85fbb910f5e_add_scene_info.py
# Compiled at: 2018-07-28 20:23:04
# Size of source mod 2**32: 1011 bytes
"""add_scene_info

Revision ID: f85fbb910f5e
Revises: 119f5f1434f7
Create Date: 2018-07-29 10:23:04.321899

"""
revision = 'f85fbb910f5e'
down_revision = '119f5f1434f7'
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('sceneinfo', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('uuid', sa.String(length=64), nullable=True), sa.Column('label', (sa.Text()), nullable=False), sa.Column('description', (sa.Text()), nullable=False), sa.PrimaryKeyConstraint('id'))
    op.create_index((op.f('ix_sceneinfo_uuid')), 'sceneinfo', ['uuid'], unique=True)


def downgrade():
    op.drop_index((op.f('ix_sceneinfo_uuid')), table_name='sceneinfo')
    op.drop_table('sceneinfo')