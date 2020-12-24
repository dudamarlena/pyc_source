# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/ab3d66c4246e_add_cache_timeout_to_druid_cluster.py
# Compiled at: 2019-04-24 13:46:49
# Size of source mod 2**32: 1244 bytes
"""add_cache_timeout_to_druid_cluster

Revision ID: ab3d66c4246e
Revises: eca4694defa7
Create Date: 2016-09-30 18:01:30.579760

"""
revision = 'ab3d66c4246e'
down_revision = 'eca4694defa7'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('clusters', sa.Column('cache_timeout', (sa.Integer()), nullable=True))


def downgrade():
    op.drop_column('clusters', 'cache_timeout')