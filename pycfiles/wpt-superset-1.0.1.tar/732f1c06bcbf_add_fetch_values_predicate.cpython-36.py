# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/migrations/versions/732f1c06bcbf_add_fetch_values_predicate.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 1408 bytes
"""add fetch values predicate

Revision ID: 732f1c06bcbf
Revises: d6db5a5cdb5d
Create Date: 2017-03-03 09:15:56.800930

"""
revision = '732f1c06bcbf'
down_revision = 'd6db5a5cdb5d'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('datasources', sa.Column('fetch_values_from', sa.String(length=100), nullable=True))
    op.add_column('tables', sa.Column('fetch_values_predicate', sa.String(length=1000), nullable=True))


def downgrade():
    op.drop_column('tables', 'fetch_values_predicate')
    op.drop_column('datasources', 'fetch_values_from')