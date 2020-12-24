# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\d6ffdf31bdd4_add_published_column_to_dashboards.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 1391 bytes
"""Add published column to dashboards

Revision ID: d6ffdf31bdd4
Revises: b4a38aa87893
Create Date: 2018-03-30 14:00:44.929483

"""
revision = 'd6ffdf31bdd4'
down_revision = 'b4a38aa87893'
from alembic import op
import sqlalchemy as sa

def upgrade():
    with op.batch_alter_table('dashboards') as (batch_op):
        batch_op.add_column(sa.Column('published', (sa.Boolean()), nullable=True))
    op.execute("UPDATE dashboards SET published='1'")


def downgrade():
    with op.batch_alter_table('dashboards') as (batch_op):
        batch_op.drop_column('published')