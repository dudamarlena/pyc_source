# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/migrations/versions/1296d28ec131_druid_exports.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 1246 bytes
"""Adds params to the datasource (druid) table

Revision ID: 1296d28ec131
Revises: 6414e83d82b7
Create Date: 2016-12-06 17:40:40.389652

"""
revision = '1296d28ec131'
down_revision = '6414e83d82b7'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('datasources', sa.Column('params', sa.String(length=1000), nullable=True))


def downgrade():
    op.drop_column('datasources', 'params')